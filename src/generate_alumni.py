import pandas as pd
import random
import os

# --- KONFIGURASI ---
OUTPUT_PATH = "data/external/alumni.csv"
JUMLAH_ALUMNI = 2000

# --- DATASET GENERATOR (KHAS INDONESIA & UB) ---
first_names = [
    "Budi", "Siti", "Rizky", "Dewi", "Andi", "Fajar", "Nina", "Dimas", "Rina", "Agus", 
    "Putri", "Bayu", "Citra", "Eko", "Gita", "Hadi", "Indah", "Joko", "Kartika", "Lestari",
    "Aditya", "Bagas", "Cahya", "Dinda", "Erlangga", "Farhan", "Gilang", "Hana", "Irfan", "Julia",
    "Kevin", "Laras", "Mahendra", "Nadia", "Okta", "Pandu", "Qori", "Radit", "Sarah", "Tegar",
    "Utomo", "Vina", "Wahyu", "Xena", "Yoga", "Zahra", "Arif", "Bella", "Chandra", "Desi"
]

last_names = [
    "Santoso", "Aminah", "Pratama", "Lestari", "Wijaya", "Nugroho", "Kartika", "Anggara", "Kurnia", "Setiawan",
    "Puspa", "Saputra", "Wulandari", "Susanto", "Permata", "Kusuma", "Hidayat", "Prasetyo", "Utami", "Firmansyah",
    "Aditama", "Budiman", "Cahyono", "Darmawan", "Efendi", "Fauzi", "Gunawan", "Hartono", "Irawan", "Jaya",
    "Kusumo", "Laksana", "Maulana", "Nasution", "Oktaviani", "Pangestu", "Qodir", "Rahmawati", "Siregar", "Tanjung",
    "Utama", "Vebrianto", "Wibowo", "Yulianto", "Zulkarnain", "Suharto", "Widodo", "Baswedan", "Yudhoyono", "Soekarno"
]

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

# --- NAMA PERUSAHAAN SESUAI HASIL SCRAPING ---
companies = [
    # Top Real Companies (Hasil Scrape JobStreet)
    "PT Bank Danamon Indonesia, Tbk", "PT Solusi Transportasi Indonesia", "PT Trinusa Travelindo",
    "JAPFA FOOD INDONESIA", "PT CFU Technology Indonesia", "PT. Trimegah Sekuritas Indonesia, Tbk",
    "PT Japfa Comfeed Indonesia, Tbk", "PT Tsubaki Indonesia Manufacturing", "Xiaomi Technology",
    "PT MAS ARYA INDONESIA", "PT DCI Indonesia, Tbk", "PT SMART,Tbk", "PT Indocyber Global Teknologi",
    "PT Kapal Api Global", "PT Bank KEB Hana Indonesia", "PT. Bank KEB Hana Indonesia",
    "PHINTRACO GROUP", "PT Penerbit Erlangga", "PT Handal Guna Sarana", 
    
    # Data Fallback 
    "PT Mencari Cinta Sejati", "CV Maju Mundur", "PT Sumber Rejeki", 
    "StartUp Gagal Bangkit", "PT Sejahtera Abadi",
    
    # Brand Populer
    "Gojek", "Tokopedia", "Shopee", "Bank BCA", "Bank Mandiri", "Telkom Indonesia"
]

positions = [
    "Senior Staff", "Junior Staff", "Manager", "Head of Department", "Specialist", 
    "Engineer", "Analyst", "Officer", "Consultant", "Supervisor", "Management Trainee"
]

def generate_alumni_data():
    data = []
    for i in range(1, JUMLAH_ALUMNI + 1):
        # Generate ID UB (4 digit: UB0001 - UB2000)
        alumni_id = f"UB{str(i).zfill(4)}" 
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        major = random.choice(majors)
        company = random.choice(companies)
        
        # Logic: Kalau jurusan IT, posisinya IT. Kalau bukan, General.
        if major in ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", "Teknologi Informasi"]:
            pos_prefix = random.choice(["Software Engineer", "Data Scientist", "Product Manager", "DevOps", "IT Support"])
            position = f"{random.choice(['Senior', 'Junior', 'Lead'])} {pos_prefix}"
        else:
            position = f"{random.choice(positions)} {random.choice(['Marketing', 'Finance', 'HR', 'Operations', 'Sales', 'Admin'])}"

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
    print(f"🎓 Generating {JUMLAH_ALUMNI} Data Alumni UB...")
    alumni_data = generate_alumni_data()
    
    df = pd.DataFrame(alumni_data)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Berhasil membuat {len(df)} data alumni di: {OUTPUT_PATH}")
    print("Contoh 5 Data Teratas:")
    print(df.head())