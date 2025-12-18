from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os

# --- INISIALISASI APP ---
app = FastAPI(
    title="UB-LinkOps API",
    description="API Rekomendasi Karir dengan Alumni Boosting",
    version="1.0"
)

# --- GLOBAL VARIABLES (Load Once) ---
print("⏳ Loading Models & Data... (Tunggu sebentar)")

# 1. Load Model SBERT (Kita pakai yang terbaik dari eksperimen: all-MiniLM-L6-v2)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load Data Lowongan (Processed)
JOBS_PATH = "data/processed/jobs_clean.csv"
if os.path.exists(JOBS_PATH):
    jobs_df = pd.read_csv(JOBS_PATH)
    # Pre-calculate Embeddings agar API cepat (tidak hitung ulang tiap request)
    job_embeddings = model.encode(jobs_df['clean_text'].tolist(), convert_to_tensor=True)
else:
    print("⚠️ Warning: Data Jobs tidak ditemukan!")
    jobs_df = pd.DataFrame()
    job_embeddings = None

# 3. Load Data Alumni
ALUMNI_PATH = "data/external/alumni.csv"
if os.path.exists(ALUMNI_PATH):
    alumni_df = pd.read_csv(ALUMNI_PATH)
    # Buat set unik perusahaan alumni agar pencarian cepat (O(1))
    alumni_companies = set(alumni_df['company'].str.lower().unique())
else:
    print("⚠️ Warning: Data Alumni tidak ditemukan!")
    alumni_companies = set()

print("✅ System Ready!")

# --- SCHEMA INPUT/OUTPUT ---
class CVRequest(BaseModel):
    student_name: str
    major: str
    cv_text: str

# --- ENDPOINT UTAMA ---
@app.post("/match")
async def match_career(request: CVRequest):
    if jobs_df.empty:
        raise HTTPException(status_code=500, detail="Database Lowongan Kosong")

    # 1. Vektorisasi CV Mahasiswa
    cv_vector = model.encode(request.cv_text, convert_to_tensor=True)

    # 2. Hitung Semantic Similarity (Cosine Similarity)
    # Hasilnya adalah array skor kemiripan (0.0 - 1.0)
    cosine_scores = util.cos_sim(cv_vector, job_embeddings)[0]

    recommendations = []
    
    # 3. Iterasi Hasil & Terapkan Alumni Boosting
    for i, score in enumerate(cosine_scores):
        score = float(score)
        company_name = str(jobs_df.iloc[i]['company'])
        
        # Cek apakah ada alumni di perusahaan ini
        # (Kita normalize ke lowercase agar match lebih akurat)
        has_alumni = company_name.lower() in alumni_companies
        
        # --- ALUMNI BOOSTING ALGORITHM ---
        # Jika ada alumni, tambah skor relevansi sebesar 15%
        final_score = score * 1.15 if has_alumni else score
        
        # Hanya ambil yang relevansinya di atas ambang batas (misal 0.3)
        if final_score > 0.3:
            recommendations.append({
                "job_id": str(jobs_df.iloc[i]['job_id']),
                "title": jobs_df.iloc[i]['title'],
                "company": company_name,
                "location": jobs_df.iloc[i]['location'],
                "match_score": round(final_score, 4), # Skor akhir
                "original_score": round(score, 4),    # Skor murni NLP
                "alumni_boost": has_alumni            # Flag penanda
            })

    # 4. Urutkan berdasarkan skor tertinggi & Ambil Top 5
    recommendations = sorted(recommendations, key=lambda x: x['match_score'], reverse=True)[:5]

    return {
        "status": "success",
        "student": request.student_name,
        "recommendations": recommendations
    }

# Untuk menjalankan via terminal:
# uvicorn src.main_api:app --reload