import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_helper import main

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    query: str

def get_cocktail_recommendation(query):
    return main(query)

@app.get("/", response_class=HTMLResponse)
async def serve_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend")
async def recommend(query_request: QueryRequest):
    recommendation = get_cocktail_recommendation(query_request.query)
    return {"recommendation": recommendation}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
