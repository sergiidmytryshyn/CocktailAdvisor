import os
import faiss
import numpy as np
import pandas as pd
from openai import OpenAI
from sentence_transformers import SentenceTransformer

API_KEY = ""
DATA_PATH = "data/final_cocktails.csv"
client = OpenAI(api_key=API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")


def preprocess_data(path):
    df = pd.read_csv(path)
    columns = ["name", "alcoholic", "category", "glassType", "instructions", "ingredients", "ingredientMeasures"]

    df = df[columns]
    df = df.dropna()

    df["ingredients"] = df["ingredients"].apply(lambda x: x[1:-1].replace("'","").split(", ") if isinstance(x, str) else [])
    df["ingredientMeasures"] = df["ingredientMeasures"].apply(lambda x: x[1:-1].replace("'","").split(", ") if isinstance(x, str) else [])
    df["description"] = df.apply(lambda row: f"{row['name']} - {row['category']}, {row['alcoholic']}. " +
                                            f"Ingredients and proportions: {str(list(map(lambda x: f'{x[0]}of {x[1]}', zip(row['ingredientMeasures'], row['ingredients']))))[1:-1]}".replace("'","") +
                                            f". Instructions: {row['instructions']} Served in {row['glassType']}.", axis=1)
    return df

def get_cocktails(query, top_k=5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in range(top_k):
        desc = cocktail_descriptions[indices[0][i]]
        results.append(desc)
    return results

if not (os.path.exists("data/cocktail_names.npy") and os.path.exists("data/cocktail_descriptions.npy")):
    df = preprocess_data(DATA_PATH)
    cocktail_names = df["name"].tolist()
    cocktail_descriptions = df["description"].tolist()
    np.save("data/cocktail_names.npy", np.array(cocktail_names))
    np.save("data/cocktail_descriptions.npy", np.array(cocktail_descriptions))
else:
    cocktail_names = np.load("data/cocktail_names.npy", allow_pickle=True)
    cocktail_descriptions = np.load("data/cocktail_descriptions.npy", allow_pickle=True)

if not os.path.exists("data/user_history.npy"):
    np.save("data/user_history.npy", np.array([]))

if not os.path.exists("data/faiss_cocktails.index"):
    embeddings = model.encode(df["description"].tolist(), convert_to_numpy=True)
    d = embeddings.shape[1]

    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    faiss.write_index(index, "data/faiss_cocktails.index")
else:
    index = faiss.read_index("data/faiss_cocktails.index")


def update_user_history(query):
    user_history = np.load("data/user_history.npy", allow_pickle=True)
    user_history = np.append(user_history, query)
    user_embedding = model.encode(user_history, convert_to_numpy=True)
    user_d = user_embedding.shape[1]
    user_index = faiss.IndexFlatL2(user_d)
    user_index.add(user_embedding)

    faiss.write_index(user_index, "data/faiss_user.index")
    np.save("data/user_history.npy", np.array(user_history))
    return user_index, user_history

def get_user_preferrences(u_index, user_history, top_k=3):
    queries = ["I like this", "I hate this"]
    preferrences = []
    for query in queries:
        query_embedding = model.encode([query], convert_to_numpy=True)
        distances, indices = u_index.search(query_embedding, top_k)
        preferrence = []
        for i in range(top_k):
            if distances[0][i] < 1.5:
                msg = user_history[indices[0][i]]
                if msg not in preferrence:
                    preferrence.append(msg)
        preferrences.append(preferrence)
    return preferrences

def generate_cocktail_response(user_query, cocktails, user_preferrences):
    prompt = f"""
    User wants a cocktail recommendation. User's query: "{user_query}", here are relevant cocktails:
    {", ".join(cocktails)}. 

    Generate a cocktail recommendation take into account user's prefferences:""" f"{str(user_preferrences[0])[1:-1]}. {str(user_preferrences[1])[1:-1]}."
    response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "system", "content": "You are a cocktail recommendation assistant."},
              {"role": "user", "content": prompt}])

    return response.choices[0].message.content

def main(user_input):
    user_index, user_history = update_user_history(user_input)
    prefs = get_user_preferrences(user_index, user_history)
    cocktails = get_cocktails(user_input)  
    response = generate_cocktail_response(user_input, cocktails, prefs)      
    return response

