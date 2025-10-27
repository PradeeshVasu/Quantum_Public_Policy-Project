# ---------- Libraries ----------
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import textwrap
import os

# ---------- Load Models + Data ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Education Model ----------
EDU_MODEL_PATH = os.path.join(BASE_DIR, "policy_vectorizer.pkl")
EDU_MATRIX_PATH = os.path.join(BASE_DIR, "policy_tfidf_matrix.pkl")
edu_vectorizer = joblib.load(EDU_MODEL_PATH)
edu_data = joblib.load(EDU_MATRIX_PATH)
edu_tfidf_matrix = edu_data["matrix"]
edu_df = edu_data["df"]

# ---------- Poverty Model ----------
POV_MODEL_PATH = os.path.join(BASE_DIR, "poverty_vectorizer.pkl")
POV_MATRIX_PATH = os.path.join(BASE_DIR, "poverty_tfidf_matrix.pkl")
pov_vectorizer = joblib.load(POV_MODEL_PATH)
pov_data = joblib.load(POV_MATRIX_PATH)
pov_tfidf_matrix = pov_data["matrix"]
pov_df = pov_data["df"]

# ---------- Government Scheme Model ----------
SCHEME_MODEL_PATH = os.path.join(BASE_DIR, "scheme_vectorizer.pkl")
SCHEME_MATRIX_PATH = os.path.join(BASE_DIR, "scheme_tfidf_matrix.pkl")
scheme_vectorizer = joblib.load(SCHEME_MODEL_PATH)
scheme_data = joblib.load(SCHEME_MATRIX_PATH)
scheme_tfidf_matrix = scheme_data["matrix"]
scheme_df = scheme_data["df"]

# ---------- FastAPI App Setup ----------
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- Search Functions ----------
def search_education(query: str, top_k: int = 3):
    query_vec = edu_vectorizer.transform([query.lower()])
    sims = cosine_similarity(query_vec, edu_tfidf_matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    results = []
    for idx in top_idx:
        row = edu_df.iloc[idx]
        results.append({
            "title": row["title"],
            "policy_id": row["policy_id"],
            "region": row["region"],
            "year": row["year"],
            "status": row["status"],
            "summary": textwrap.shorten(row["full_text"], width=250, placeholder="..."),
            "score": round(sims[idx], 3),
            "impact_score": row.get("impact_score", 0),
            "funding_million_usd": row.get("funding_million_usd", 0)
        })
    return results

def search_poverty(query: str, top_k: int = 3):
    query_vec = pov_vectorizer.transform([query.lower()])
    sims = cosine_similarity(query_vec, pov_tfidf_matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    results = []
    for idx in top_idx:
        row = pov_df.iloc[idx]
        results.append({
            "State": row["State"],
            "Rural 2011-12 Poverty Expenditure Per Capita": row["Rural 2011-12 Poverty Expenditure Per Capita"],
            "Urban 2011-12 Poverty Expenditure Per Capita": row["Urban 2011-12 Poverty Expenditure Per Capita"],
            "Headcount Ratio (%)": row["Headcount Ratio (%)"],
            "2011 rural percentage": row["2011 rural percentage"],
            "FII Rank": row["FII Rank"],
            "CFII": row["CFII"],
            "CDI": row["CDI"],
            "summary": textwrap.shorten(str(row["State"]) + " poverty info.", width=250, placeholder="..."),
            "Similarity": round(sims[idx], 3)
        })
    return results

def search_scheme(query: str, top_k: int = 3):
    query_vec = scheme_vectorizer.transform([query.lower()])
    sims = cosine_similarity(query_vec, scheme_tfidf_matrix).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    results = []
    for idx in top_idx:
        row = scheme_df.iloc[idx]
        results.append({
            "scheme_name": row.get("scheme_name", "N/A"),
            "details": row.get("details", "N/A"),
            "benefits": row.get("benefits", "N/A"),
            "eligibility": row.get("eligibility", "N/A"),
            "application": row.get("application", "N/A"),
            "documents": row.get("documents", "N/A"),
            "level": row.get("level", "N/A"),
            "schemeCategory": row.get("schemeCategory", "N/A"),
            "tags": row.get("tags", "N/A"),
            "summary": textwrap.shorten(str(row.get("details", "")), width=250, placeholder="..."),
            "score": round(sims[idx], 3)
        })
    return results

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

# Education
@app.post("/search_education", response_class=HTMLResponse)
async def search_education_route(request: Request, query: str = Form(...)):
    results = search_education(query)
    return templates.TemplateResponse("education.html", {"request": request, "results": results, "query": query})

@app.get("/call_education", response_class=HTMLResponse)
async def call_edu(request: Request):
    return templates.TemplateResponse("education.html", {"request": request, "results": None})

# Poverty
@app.post("/search_poverty", response_class=HTMLResponse)
async def search_poverty_route(request: Request, query: str = Form(...)):
    results = search_poverty(query)
    return templates.TemplateResponse("poverty.html", {"request": request, "results": results, "query": query})

@app.get("/call_poverty", response_class=HTMLResponse)
async def call_pov(request: Request):
    return templates.TemplateResponse("poverty.html", {"request": request, "results": None})

# Government Schemes
@app.post("/search_scheme", response_class=HTMLResponse)
async def search_scheme_route(request: Request, query: str = Form(...)):
    results = search_scheme(query)
    return templates.TemplateResponse("gov_scheme.html", {"request": request, "results": results, "query": query})

@app.get("/call_scheme", response_class=HTMLResponse)
async def call_scheme(request: Request):
    return templates.TemplateResponse("gov_scheme.html", {"request": request, "results": None})

