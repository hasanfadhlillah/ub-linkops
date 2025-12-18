import pandas as pd
import re
import os

# --- KONFIGURASI ---
INPUT_PATH = "data/raw/jobs_data.csv"
OUTPUT_PATH = "data/processed/jobs_clean.csv"

def clean_text(text):
    """Membersihkan teks dari HTML tags, simbol, dan lowercase."""
    if not isinstance(text, str):
        return ""
    
    # 1. Hapus HTML Tags (misal: <br>, <div>)
    text = re.sub(r'<.*?>', ' ', text)
    
    # 2. Hapus karakter non-alphanumeric (kecuali spasi)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # 3. Case Folding (Huruf kecil semua)
    text = text.lower()
    
    # 4. Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def run_preprocessing():
    print("🧹 Memulai Data Preprocessing...")
    
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Error: File {INPUT_PATH} tidak ditemukan. Jalankan scraper dulu!")
        return

    # Load Data Raw
    df = pd.read_csv(INPUT_PATH)
    print(f"📊 Data Awal: {len(df)} baris")

    # Drop Duplikat berdasarkan Job ID
    df = df.drop_duplicates(subset=['job_id'])
    
    # Proses Pembersihan
    # Kita gabungkan Title + Description agar konteksnya lebih kaya untuk AI
    df['clean_text'] = df['title'].apply(clean_text) + " " + df['description'].apply(clean_text)
    
    # Pastikan folder output ada
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Simpan
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Data Bersih Disimpan: {OUTPUT_PATH} ({len(df)} baris)")

if __name__ == "__main__":
    run_preprocessing()