# Libraries

from fastapi import FastAPI, Request, Form

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

import joblib

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

import textwrap
 
# ---------- Load Model + Data ----------
 
 
MODEL_PATH = "policy_vectorizer.pkl"

MATRIX_PATH = "policy_tfidf_matrix.pkl"

vectorizer = joblib.load(MODEL_PATH)

data = joblib.load(MATRIX_PATH)

tfidf_matrix = data["matrix"] 

df = data["df"]
 
# ---------- FastAPI App Setup ----------

app = FastAPI()
 
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
 
 
def search_policies(query: str, top_k: int = 3):

    query_vec = vectorizer.transform([query.lower()])

    sims = cosine_similarity(query_vec, tfidf_matrix).flatten()

    top_idx = sims.argsort()[::-1][:top_k]
 
    results = []

    for idx in top_idx:

        row = df.iloc[idx]

        results.append({

            "title": row["title"],

            "policy_id": row["policy_id"],

            "region": row["region"],

            "year": row["year"],

            "status": row["status"],

            "summary": textwrap.shorten(row["full_text"], width=250, placeholder="..."),

            "score": round(sims[idx], 3)

        })

    return results
 
 
@app.get("/", response_class=HTMLResponse)

async def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "results": None})
 
 
@app.post("/search", response_class=HTMLResponse)

async def search(request: Request, query: str = Form(...)):

    results = search_policies(query)

    return templates.TemplateResponse("index.html", {"request": request, "results": results, "query": query})

 
