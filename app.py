from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import textwrap
import os
import logging
import warnings
import pennylane as qml
from pennylane import numpy as pnp
import sklearn

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check scikit-learn version
logger.info(f"scikit-learn version: {sklearn.__version__}")

# Load Models + Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Education Model
try:
    EDU_MODEL_PATH = os.path.join(BASE_DIR, "policy_vectorizer.pkl")
    EDU_MATRIX_PATH = os.path.join(BASE_DIR, "policy_tfidf_matrix.pkl")
    if not os.path.exists(EDU_MODEL_PATH) or not os.path.exists(EDU_MATRIX_PATH):
        raise FileNotFoundError(f"Education model files not found: {EDU_MODEL_PATH}, {EDU_MATRIX_PATH}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        edu_vectorizer = joblib.load(EDU_MODEL_PATH)
        edu_data = joblib.load(EDU_MATRIX_PATH)
    edu_tfidf_matrix = edu_data["matrix"]
    edu_df = edu_data["df"]
    logger.info("✅ Education Model Loaded Successfully!")
except Exception as e:
    logger.warning(f"⚠️ Failed to load Education Model: {str(e)}. Disabling Education model search.")
    edu_vectorizer = None
    edu_tfidf_matrix = None
    edu_df = None

# Poverty Model
try:
    POV_MODEL_PATH = os.path.join(BASE_DIR, "poverty_vectorizer.pkl")
    POV_MATRIX_PATH = os.path.join(BASE_DIR, "poverty_tfidf_matrix.pkl")
    if not os.path.exists(POV_MODEL_PATH) or not os.path.exists(POV_MATRIX_PATH):
        raise FileNotFoundError(f"Poverty model files not found: {POV_MODEL_PATH}, {POV_MATRIX_PATH}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        pov_vectorizer = joblib.load(POV_MODEL_PATH)
        pov_data = joblib.load(POV_MATRIX_PATH)
    pov_tfidf_matrix = pov_data["matrix"]
    pov_df = pov_data["df"]
    logger.info("✅ Poverty Model Loaded Successfully!")
except Exception as e:
    logger.warning(f"⚠️ Failed to load Poverty Model: {str(e)}. Disabling Poverty model search.")
    pov_vectorizer = None
    pov_tfidf_matrix = None
    pov_df = None

# Government Scheme Model
try:
    SCHEME_MODEL_PATH = os.path.join(BASE_DIR, "scheme_vectorizer.pkl")
    SCHEME_MATRIX_PATH = os.path.join(BASE_DIR, "scheme_tfidf_matrix.pkl")
    if not os.path.exists(SCHEME_MODEL_PATH) or not os.path.exists(SCHEME_MATRIX_PATH):
        raise FileNotFoundError(f"Scheme model files not found: {SCHEME_MODEL_PATH}, {SCHEME_MATRIX_PATH}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        scheme_vectorizer = joblib.load(SCHEME_MODEL_PATH)
        scheme_data = joblib.load(SCHEME_MATRIX_PATH)
    scheme_tfidf_matrix = scheme_data["matrix"]
    scheme_df = scheme_data["df"]
    logger.info("✅ Government Scheme Model Loaded Successfully!")
except Exception as e:
    logger.warning(f"⚠️ Failed to load Government Scheme Model: {str(e)}. Disabling Scheme model search.")
    scheme_vectorizer = None
    scheme_tfidf_matrix = None
    scheme_df = None

# Quantum Education Model
try:
    logger.info("🔍 Loading Quantum Model Pickle Files...")
    QUANTUM_MODEL_PATH = os.path.join(BASE_DIR, "policy_vectorizer_quantum.pkl")
    QUANTUM_MATRIX_PATH = os.path.join(BASE_DIR, "policy_tfidf_matrix_quantum.pkl")

    if not os.path.exists(QUANTUM_MODEL_PATH):
        raise FileNotFoundError(f"Quantum vectorizer file not found: {os.path.abspath(QUANTUM_MODEL_PATH)}")
    if not os.path.exists(QUANTUM_MATRIX_PATH):
        raise FileNotFoundError(f"Quantum matrix file not found: {os.path.abspath(QUANTUM_MATRIX_PATH)}")

    quantum_vectorizer = joblib.load(QUANTUM_MODEL_PATH)
    quantum_data = joblib.load(QUANTUM_MATRIX_PATH)

    logger.info(f"Quantum data type: {type(quantum_data)}")
    logger.info(f"Quantum data keys: {list(quantum_data.keys()) if isinstance(quantum_data, dict) else 'Not a dict'}")

    # Extract data with proper key handling
    quantum_tfidf_matrix = quantum_data.get("matrix", quantum_data.get("tfidf_matrix"))
    quantum_normalized_vectors = quantum_data.get("normalized_vectors")
    quantum_df = quantum_data.get("df")

    # Validate data (avoid boolean evaluation of arrays)
    if quantum_tfidf_matrix is None:
        logger.error("Quantum TF-IDF matrix is missing.")
        raise ValueError("Quantum TF-IDF matrix is missing.")
    if quantum_normalized_vectors is None:
        logger.error("Quantum normalized vectors are missing.")
        raise ValueError("Quantum normalized vectors are missing.")
    if quantum_df is None or not isinstance(quantum_df, pd.DataFrame):
        logger.error("Quantum DataFrame is missing or invalid.")
        raise ValueError("Quantum DataFrame is missing or invalid.")

    # Verify DataFrame columns
    required_columns = ['title', 'policy_id', 'region', 'year', 'status', 'text_for_nlp', 'impact_score', 'funding_million_usd', 'stakeholders']
    missing_columns = [col for col in required_columns if col not in quantum_df.columns]
    if missing_columns:
        logger.warning(f"Missing DataFrame columns: {missing_columns}. Using defaults.")
        for col in missing_columns:
            quantum_df[col] = quantum_df.get(col, 'N/A' if col in ['title', 'policy_id', 'region', 'status', 'text_for_nlp', 'stakeholders'] else 0.0)

    # Quantum device setup
    n_qubits = 3
    quantum_dev = qml.device("default.qubit", wires=n_qubits)

    def feature_map(vec):
        norm = pnp.linalg.norm(vec)
        if norm == 0:
            vec = pnp.ones_like(vec) / pnp.sqrt(len(vec))
        qml.AmplitudeEmbedding(vec, wires=range(n_qubits), normalize=True)
        qml.BasicEntanglerLayers(pnp.random.random((2, n_qubits)), wires=range(n_qubits))

    @qml.qnode(quantum_dev)
    def kernel_circuit(v1, v2):
        feature_map(v1)
        qml.adjoint(feature_map)(v2)
        return qml.probs(wires=range(n_qubits))

    logger.info("✅ Quantum Model Loaded Successfully!")
    logger.info(f" - Matrix shape: {quantum_tfidf_matrix.shape if quantum_tfidf_matrix is not None else 'N/A'}")
    logger.info(f" - Normalized vectors shape: {quantum_normalized_vectors.shape if quantum_normalized_vectors is not None else 'N/A'}")
    logger.info(f" - DataFrame rows: {len(quantum_df)}")
    logger.info(f" - DataFrame columns: {list(quantum_df.columns)}")

except Exception as e:
    logger.error(f"❌ Failed to load Quantum Model: {str(e)}")
    quantum_vectorizer = None
    quantum_tfidf_matrix = None
    quantum_normalized_vectors = None
    quantum_df = pd.DataFrame({
        'title': ['Placeholder Policy'],
        'policy_id': ['QP000'],
        'region': ['N/A'],
        'year': [2023],
        'status': ['N/A'],
        'text_for_nlp': ['No quantum policy data available.'],
        'impact_score': [0.0],
        'funding_million_usd': [0.0],
        'stakeholders': ['N/A']
    })
    quantum_dev = None
    kernel_circuit = None

# FastAPI App Setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Search Functions
def search_education(query: str, top_k: int = 3):
    if edu_vectorizer is None or edu_tfidf_matrix is None or edu_df is None:
        logger.error("Education model not loaded.")
        return [{"error": "Education model not loaded."}]
    try:
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
                "score": round(float(sims[idx]), 3),
                "impact_score": float(row.get("impact_score", 0)),
                "funding_million_usd": float(row.get("funding_million_usd", 0)),
                "stakeholders": row.get("stakeholders", "N/A")
            })
        return results
    except Exception as e:
        logger.error(f"Education search failed: {str(e)}")
        return [{"error": f"Education search failed: {str(e)}"}]

def search_poverty(query: str, top_k: int = 3):
    if pov_vectorizer is None or pov_tfidf_matrix is None or pov_df is None:
        logger.error("Poverty model not loaded.")
        return [{"error": "Poverty model not loaded."}]
    try:
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
                "Similarity": round(float(sims[idx]), 3)
            })
        return results
    except Exception as e:
        logger.error(f"Poverty search failed: {str(e)}")
        return [{"error": f"Poverty search failed: {str(e)}"}]

def search_scheme(query: str, top_k: int = 3):
    if scheme_vectorizer is None or scheme_tfidf_matrix is None or scheme_df is None:
        logger.error("Scheme model not loaded.")
        return [{"error": "Scheme model not loaded."}]
    try:
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
                "score": round(float(sims[idx]), 3)
            })
        return results
    except Exception as e:
        logger.error(f"Scheme search failed: {str(e)}")
        return [{"error": f"Scheme search failed: {str(e)}"}]

def search_quantum(query: str, top_k: int = 3):
    if quantum_vectorizer is None or quantum_normalized_vectors is None or quantum_df is None or kernel_circuit is None:
        logger.error("Quantum model not loaded.")
        return [{"error": "Quantum model not loaded."}]
    try:
        logger.info(f"Processing quantum query: {query}")
        query_tfidf = quantum_vectorizer.transform([query.lower()]).toarray()[0]
        norm = pnp.linalg.norm(query_tfidf)
        query_vec = query_tfidf / norm if norm > 0 else pnp.ones_like(query_tfidf) / pnp.sqrt(len(query_tfidf))
        sims = pnp.array([kernel_circuit(query_vec, quantum_normalized_vectors[i])[0] for i in range(quantum_normalized_vectors.shape[0])])
        top_idx = sims.argsort()[::-1][:top_k]
        results = []
        for idx in top_idx:
            row = quantum_df.iloc[idx]
            results.append({
                "title": row.get("title", "N/A"),
                "policy_id": row.get("policy_id", "N/A"),
                "region": row.get("region", "N/A"),
                "year": row.get("year", "N/A"),
                "status": row.get("status", "N/A"),
                "summary": textwrap.shorten(str(row.get("text_for_nlp", row.get("full_text", ""))), width=250, placeholder="..."),
                "score": round(float(sims[idx]), 3),
                "impact_score": float(row.get("impact_score", 0)),
                "funding_million_usd": float(row.get("funding_million_usd", 0)),
                "stakeholders": row.get("stakeholders", "N/A")
            })
        logger.info(f"Quantum search returned {len(results)} results")
        return results
    except Exception as e:
        logger.error(f"Quantum search failed: {str(e)}")
        return [{"error": f"Quantum search failed: {str(e)}"}]

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/search_education", response_class=HTMLResponse)
async def search_education_route(request: Request, query: str = Form(...)):
    results = search_education(query)
    return templates.TemplateResponse("education.html", {"request": request, "results": results, "query": query})

@app.get("/call_education", response_class=HTMLResponse)
async def call_edu(request: Request):
    return templates.TemplateResponse("education.html", {"request": request, "results": None})

@app.post("/search_poverty", response_class=HTMLResponse)
async def search_poverty_route(request: Request, query: str = Form(...)):
    results = search_poverty(query)
    return templates.TemplateResponse("poverty.html", {"request": request, "results": results, "query": query})

@app.get("/call_poverty", response_class=HTMLResponse)
async def call_pov(request: Request):
    return templates.TemplateResponse("poverty.html", {"request": request, "results": None})

@app.post("/search_scheme", response_class=HTMLResponse)
async def search_scheme_route(request: Request, query: str = Form(...)):
    results = search_scheme(query)
    return templates.TemplateResponse("gov_scheme.html", {"request": request, "results": results, "query": query})

@app.get("/call_scheme", response_class=HTMLResponse)
async def call_scheme(request: Request):
    return templates.TemplateResponse("gov_scheme.html", {"request": request, "results": None})

@app.post("/search_quantum", response_class=HTMLResponse)
async def search_quantum_route(request: Request, query: str = Form(...)):
    results = search_quantum(query)
    return templates.TemplateResponse("quantum_edu.html", {"request": request, "results": results, "query": query})

@app.get("/call_quantum", response_class=HTMLResponse)
async def call_quantum(request: Request):
    return templates.TemplateResponse("quantum_edu.html", {"request": request, "results": None})