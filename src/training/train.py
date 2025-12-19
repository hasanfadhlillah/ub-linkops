import pandas as pd
from sentence_transformers import SentenceTransformer
import mlflow
import os
import time

# --- 1. KONFIGURASI PINTAR (SMART CONFIG) ---
# Cek apakah script sedang jalan di GitHub Actions (CI) atau di Laptop (Local)
IS_IN_CI = os.getenv("GITHUB_ACTIONS") == "true"

if IS_IN_CI:
    # KASUS A: Jalan di GitHub Actions
    # Kita set tracking ke folder lokal saja, biar gak nyari server yang mati
    print("🤖 Terdeteksi berjalan di CI Pipeline. Menggunakan Local Storage.")
    mlflow.set_tracking_uri("file:./mlruns")
else:
    # KASUS B: Jalan di Laptop (Docker)
    # Kita tembak ke MLflow Server container
    TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    print(f"🖥️ Terdeteksi berjalan di Docker/Local. Menggunakan Server: {TRACKING_URI}")
    mlflow.set_tracking_uri(TRACKING_URI)

MLFLOW_EXPERIMENT_NAME = "UB-LinkOps_SBERT_Comparison"

def run_experiment():
    print(f"🧪 Memulai Eksperimen Model SBERT...")
    
    # Set Experiment
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    with mlflow.start_run():
        # --- 2. LOAD DATA (SMART LOAD) ---
        documents = []
        if IS_IN_CI:
            # Kalau di CI, pakai data dummy biar cepat & gak butuh file CSV
            print("⚠️ Mode CI: Menggunakan Dummy Data.")
            documents = ["Lowongan dummy 1", "Lowongan dummy 2"] * 5
        else:
            # Kalau di Laptop, coba load data asli
            try:
                csv_path = "data/processed/jobs_clean.csv"
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    # Ambil sampel 100 data aja buat testing training biar cepet
                    documents = df['clean_text'].tolist()[:100] 
                    print(f"✅ Data asli ditemukan: {len(documents)} baris sample.")
                else:
                    print("⚠️ File CSV tidak ditemukan, fallback ke dummy.")
                    documents = ["Dummy job description"] * 10
            except Exception as e:
                print(f"⚠️ Gagal load data: {e}")
                documents = ["Dummy job description"] * 10

        # --- 3. TRAINING / EMBEDDING ---
        model_name = 'all-MiniLM-L6-v2'
        start_time = time.time()
        
        model = SentenceTransformer(model_name)
        embeddings = model.encode(documents)
        
        duration = time.time() - start_time
        
        # --- 4. LOG METRICS (LOGIKA KAMU YANG BENAR) ---
        print("📝 Logging metrics ke MLflow...")
        
        # Log Parameter
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("data_count", len(documents))
        
        # Log Metrik Kinerja
        mlflow.log_metric("embedding_time_sec", duration)
        
        # Hindari pembagian dengan nol
        if len(documents) > 0:
            mlflow.log_metric("seconds_per_doc", duration / len(documents))
        
        print(f"✅ Eksperimen Selesai! Durasi: {duration:.4f} detik")

if __name__ == "__main__":
    run_experiment()