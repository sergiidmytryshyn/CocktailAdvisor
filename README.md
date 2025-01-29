# CocktailAdvisor

## Installation

1. Get your API Key at https://platform.openai.com/settings/organization/api-keys
2. Clone repository
```
git clone https://github.com/sergiidmytryshyn/CocktailAdvisor.git
```
3. Install Python packages
```
pip install -r requirements.txt
```
## Usage
1. Insert your OPENAI API KEY in rag_helper.py
2. In repository directory run
```
python3 server.py
```
3. Go to http://0.0.0.0:8080/

## Summary
From images below we can see that my assistant works properly and satisfies the requirements.  <br>
<img width="450" alt="Screenshot 2025-01-29 at 20 25 21" src="https://github.com/user-attachments/assets/9a3a93c0-d3c2-4756-ada1-f6bcfa1542d0" /> 

<img width="450" alt="Screenshot 2025-01-29 at 20 27 01" src="https://github.com/user-attachments/assets/b7905ca4-1af9-4a3b-abf8-0e6d2246d04e" />

<img width="500" alt="Screenshot 2025-01-29 at 20 31 09" src="https://github.com/user-attachments/assets/c89174d3-173f-444e-bcfc-4f630df7c9ae" />

<img width="512" alt="Screenshot 2025-01-29 at 20 46 56" src="https://github.com/user-attachments/assets/27074e6f-2c4c-4a8d-9ea6-10645d71ae08" />

<img width="519" alt="Screenshot 2025-01-29 at 20 58 49" src="https://github.com/user-attachments/assets/7b1837c7-dc76-46c2-930e-0df0118c77b8" />

<img width="502" alt="Screenshot 2025-01-29 at 21 00 04" src="https://github.com/user-attachments/assets/d5973d3a-51bd-4028-817e-8ab7ac71efa9" />

<img width="468" alt="Screenshot 2025-01-29 at 21 02 27" src="https://github.com/user-attachments/assets/76e87e3a-e632-4828-97eb-38c4e2e247ff" />

The biggest problem was user's preferrences. Firstly I thought to get it by feeding each prompt to LLM, but it is too expensive from computaional point of view. So I just Compare each query with phrases "I like this" and "I dont like this.". I agree that these sentences are not very good and my assistant is not able to take preferrences from complex queries, but it works with simple. Also I firsty passed only names of retrieved cocktails, but then I started passing whole description of each drink in order to make response more detailed, but of course each prompt become more expensive due to incresement of input tokens. 
