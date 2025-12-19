from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="UB-LinkOps API (Monitored)")

# --- PASANG MONITORING ---
Instrumentator().instrument(app).expose(app)

print("⏳ Loading Models & Data...")
model = SentenceTransformer('all-MiniLM-L6-v2')

JOBS_PATH = "data/jobs_clean.csv"
ALUMNI_PATH = "data/alumni.csv"

# Load Data Sekali Saja
if os.path.exists(JOBS_PATH):
    jobs_df = pd.read_csv(JOBS_PATH)
    job_embeddings = model.encode(jobs_df['clean_text'].tolist(), convert_to_tensor=True)
else:
    jobs_df = pd.DataFrame()
    job_embeddings = None

alumni_companies = set()
if os.path.exists(ALUMNI_PATH):
    alumni_df = pd.read_csv(ALUMNI_PATH)
    alumni_companies = set(alumni_df['company'].str.lower().unique())

class CVRequest(BaseModel):
    student_name: str
    major: str
    cv_text: str

@app.post("/match")
async def match_career(request: CVRequest):
    if jobs_df.empty:
        raise HTTPException(status_code=500, detail="Database Lowongan Kosong")

    # Inferensi
    cv_vector = model.encode(request.cv_text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(cv_vector, job_embeddings)[0]

    recommendations = []
    for i, score in enumerate(cosine_scores):
        score = float(score)
        company = str(jobs_df.iloc[i]['company'])
        has_alumni = company.lower() in alumni_companies
        
        final_score = score * 1.15 if has_alumni else score
        
        if final_score > 0.3:
            recommendations.append({
                "job_id": str(jobs_df.iloc[i]['job_id']),
                "title": jobs_df.iloc[i]['title'],
                "company": company,
                "location": jobs_df.iloc[i]['location'],
                "match_score": round(final_score, 4),
                "original_score": round(score, 4),
                "alumni_boost": has_alumni
            })

    top_matches = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)[:5]
    
    return {
        "status": "success",
        "student": request.student_name,
        "recommendations": top_matches
    }