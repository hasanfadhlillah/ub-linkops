import pandas as pd
import random
import os

# --- KONFIGURASI ---
OUTPUT_PATH = "data/external/alumni.csv"
JUMLAH_ALUMNI = 100  # Kita bikin 100 alumni biar kelihatan banyak database-nya

# --- DATASET GENERATOR (KHAS UB) ---
# Daftar Nama Depan & Belakang Indonesia
first_names = ["Budi", "Siti", "Rizky", "Dewi", "Andi", "Fajar", "Nina", "Dimas", "Rina", "Agus", 
               "Putri", "Bayu", "Citra", "Eko", "Gita", "Hadi", "Indah", "Joko", "Kartika", "Lestari"]
last_names = ["Santoso", "Aminah", "Pratama", "Lestari", "Wijaya", "Nugroho", "Kartika", "Anggara", "Kurnia", "Setiawan",
              "Puspa", "Saputra", "Wulandari", "Susanto", "Permata", "Kusuma", "Hidayat", "Praseyto", "Utami", "Firmansyah"]

# Daftar Jurusan di UB (Sesuai Fakultas)
majors = [
    # FILKOM
    "Teknik Informatika", "Sistem Informasi", "Teknik Komputer", "Teknologi Informasi", "Pendidikan TI",
    # FEB
    "Akuntansi", "Manajemen", "Ilmu Ekonomi", "Ekonomi Islam", "Keuangan Perbankan",
    # FT
    "Teknik Sipil", "Teknik Mesin", "Teknik Elektro", "Teknik Industri", "Arsitektur",
    # PERTANIAN & TEKNOLOGI PERTANIAN
    "Agroekoteknologi", "Agribisnis", "Teknologi Hasil Pertanian", "Teknik Lingkungan",
    # FISIP & HUKUM
    "Ilmu Hukum", "Ilmu Komunikasi", "Administrasi Publik", "Hubungan Internasional", "Psikologi"
]

# Perusahaan (Harus match sama target scraping kita biar fitur Matching jalan!)
companies = [
    "Tokopedia", "Gojek", "Traveloka", "Shopee", "Bank Jago", "Bank BCA", "Bank Mandiri", 
    "Telkom Indonesia", "Ruangguru", "Bibit.id", "Astra International", "BliBli", "Tiket.com",
    "Pertamina", "PLN", "Unilever", "Danone", "Gudang Garam", "Sampoerna"
]

positions = [
    "Senior Staff", "Junior Staff", "Manager", "Head of Department", "Specialist", 
    "Engineer", "Analyst", "Officer", "Consultant", "Supervisor"
]

def generate_alumni_data():
    data = []
    for i in range(1, JUMLAH_ALUMNI + 1):
        # Generate ID UB
        alumni_id = f"UB{str(i).zfill(3)}" # Jadinya UB001, UB002, dst
        
        # Generate Nama
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate Jurusan & Posisi
        major = random.choice(majors)
        company = random.choice(companies)
        
        # Logic dikit: Kalau jurusan IT, posisinya berbau IT. Kalau bukan, General.
        if major in ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", "Teknologi Informasi"]:
            pos_prefix = random.choice(["Software Engineer", "Data Scientist", "Product Manager", "DevOps", "IT Support"])
            position = f"{random.choice(['Senior', 'Junior', 'Lead'])} {pos_prefix}"
        else:
            position = f"{random.choice(positions)} {random.choice(['Marketing', 'Finance', 'HR', 'Operations', 'Sales'])}"

        graduation_year = random.randint(2015, 2023)
        
        data.append({
            "alumni_id": alumni_id,
            "name": name,
            "major": major,
            "company": company,
            "position": position,
            "graduation_year": graduation_year
        })
        
    return data

if __name__ == "__main__":
    print("🎓 Generating Data Alumni UB...")
    alumni_data = generate_alumni_data()
    
    df = pd.DataFrame(alumni_data)
    
    # Pastikan folder ada
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Simpan CSV
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Berhasil membuat {len(df)} data alumni di: {OUTPUT_PATH}")
    print("Contoh 5 Data Teratas:")
    print(df.head())