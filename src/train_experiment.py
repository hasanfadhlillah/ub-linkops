import pandas as pd
import time
import mlflow
import os
from sentence_transformers import SentenceTransformer

# --- KONFIGURASI ---
DATA_PATH = "data/processed/jobs_clean.csv"
MLFLOW_EXPERIMENT_NAME = "UB-LinkOps_SBERT_Comparison"

def run_experiment():
    if not os.path.exists(DATA_PATH):
        print("❌ Data processed tidak ditemukan. Jalankan src/preprocess.py dulu.")
        return

    # Load Data
    df = pd.read_csv(DATA_PATH)
    # Gunakan seluruh data clean hasil preprocessing
    documents = df['clean_text'].tolist()
    
    print(f"🧪 Memulai Eksperimen Model SBERT dengan {len(documents)} data lowongan...")

    # --- KONFIGURASI TRACKING SERVER ---
    mlflow.set_tracking_uri("http://ub-linkops-mlflow:5000") 

    # Set MLflow Experiment
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    # Daftar Model Kandidat (Kecil vs Sedang)
    models_to_test = [
        "all-MiniLM-L6-v2",           # Model kecil, sangat cepat
        "paraphrase-MiniLM-L3-v2"     # Model lebih kecil lagi, super cepat
    ]

    for model_name in models_to_test:
        with mlflow.start_run(run_name=f"Exp_{model_name}"):
            print(f"   ➡️ Testing Model: {model_name}...")
            
            start_time = time.time()
            
            # 1. Load Model
            model = SentenceTransformer(model_name)
            
            # 2. Generate Embeddings (Vektorisasi)
            embeddings = model.encode(documents)
            
            duration = time.time() - start_time
            
            # 3. Log Metrics & Params ke MLflow
            mlflow.log_param("model_name", model_name)
            mlflow.log_param("data_count", len(documents))
            mlflow.log_metric("embedding_time_sec", duration)
            mlflow.log_metric("seconds_per_doc", duration / len(documents))
            
            print(f"      ✅ Selesai dalam {duration:.2f} detik.")

    print("🏁 Eksperimen Selesai! Cek MLflow UI di http://localhost:5000 untuk detailnya.")

if __name__ == "__main__":
    run_experiment()