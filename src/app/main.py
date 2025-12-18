from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
import json
import redis
from prometheus_fastapi_instrumentator import Instrumentator

# --- INISIALISASI APP ---
app = FastAPI(
    title="UB-LinkOps Enterprise API",
    description="API dengan Redis Caching & Prometheus Monitoring",
    version="2.0"
)

# --- 1. AKTIFKAN MONITORING (Prometheus) ---
Instrumentator().instrument(app).expose(app)

# --- 2. KONEKSI REDIS CACHE ---
# Coba connect ke Redis container
try:
    redis_client = redis.Redis(host='redis-cache', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("✅ Terhubung ke Redis Cache!")
except:
    print("⚠️ Gagal konek Redis, cache dimatikan.")
    redis_client = None

# --- LOAD RESOURCES ---
print("⏳ Loading Models & Data...")
model = SentenceTransformer('all-MiniLM-L6-v2')

JOBS_PATH = "data/processed/jobs_clean.csv"
ALUMNI_PATH = "data/external/alumni.csv"

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
    # --- CEK CACHE DULU (Redis) ---
    # Kita pakai nama mahasiswa + jurusan sebagai key cache sederhana
    cache_key = f"match:{request.student_name}:{request.major}"
    
    if redis_client:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            print(f"🚀 Cache Hit untuk {request.student_name}!")
            return json.loads(cached_result)

    if jobs_df.empty:
        raise HTTPException(status_code=500, detail="Database Lowongan Kosong")

    # --- PROSES INFERENSI (Berat) ---
    cv_vector = model.encode(request.cv_text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(cv_vector, job_embeddings)[0]

    recommendations = []
    for i, score in enumerate(cosine_scores):
        score = float(score)
        company = str(jobs_df.iloc[i]['company'])
        has_alumni = company.lower() in alumni_companies
        # Jika ada alumni, tambah skor relevansi sebesar 15%
        final_score = score * 1.15 if has_alumni else score
        
        if final_score > 0.3:
            recommendations.append({
                "job_id": str(jobs_df.iloc[i]['job_id']),
                "title": jobs_df.iloc[i]['title'],
                "company": company,
                "location": jobs_df.iloc[i]['location'],
                "match_score": round(final_score, 4), # Skor akhir
                "original_score": round(score, 4),    # Skor murni NLP
                "alumni_boost": has_alumni            # Skor murni NLP
            })

    top_matches = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)[:5]
    
    response_data = {
        "status": "success",
        "source": "model_inference", # Penanda bahwa ini hasil hitung baru
        "student": request.student_name,
        "recommendations": top_matches
    }

    # --- SIMPAN KE CACHE (Redis) ---
    # Simpan hasil selama 1 jam (3600 detik) biar hemat komputasi nanti
    if redis_client:
        redis_client.setex(cache_key, 3600, json.dumps(response_data))

    return response_data