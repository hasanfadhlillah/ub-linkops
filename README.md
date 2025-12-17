# 🎓 UB-LinkOps: Intelligent Career Matcher & Alumni Network Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green?style=for-the-badge&logo=selenium)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)

> **Platform MLOps cerdas yang menjembatani mahasiswa Universitas Brawijaya dengan dunia industri melalui Semantic Matching & Analisis Jejaring Alumni.**

---

## 📖 Latar Belakang Project
**UB-LinkOps** adalah proyek akhir mata kuliah **Machine Learning Operations (MLOps)** yang bertujuan untuk menyelesaikan masalah "mismatch" antara lulusan universitas dan kebutuhan industri. 

Sistem ini tidak hanya merekomendasikan lowongan kerja berdasarkan kata kunci, tetapi menggunakan pendekatan **Hybrid Intelligence**:
1.  **Semantic Matching:** Mencocokkan konteks CV mahasiswa dengan lowongan kerja secara mendalam (bukan sekadar keyword).
2.  **Alumni Network Booster:** Memberikan prioritas rekomendasi pada perusahaan yang memiliki rekam jejak mempekerjakan alumni Universitas Brawijaya.

---

## 🚀 Fitur Unggulan (Key Features)

### 1. Continuous Data Ingestion (Hybrid Scraper)
Sistem pengumpulan data lowongan kerja yang berjalan otomatis (*background service*) dengan kemampuan:
* **Real-time Scraping:** Mengambil data langsung dari portal **JobStreet Indonesia**.
* **Inklusivitas Fakultas:** Algoritma rotasi keyword yang mencakup seluruh rumpun ilmu di UB (Teknologi, Ekonomi, Pertanian, Teknik, Sosial Hukum).
* **Fail-Safe Mechanism:** Fitur cerdas yang otomatis beralih ke *Simulated Data Generator* jika terjadi gangguan koneksi atau pemblokiran IP, menjamin pipeline data tidak pernah berhenti.

### 2. Internal Data Simulation (Alumni Database)
Generator data sintetik yang cerdas untuk mensimulasikan aset data internal kampus (Career Development Center). Data alumni disinkronisasi secara otomatis dengan perusahaan top yang ditemukan dari hasil scraping.

---

## 📂 Struktur Direktori

```text
ub-linkops/
├── data/
│   ├── raw/
│   │   └── jobs_data.csv       # Dataset Lowongan (Continuous Append)
│   ├── external/
│   │   └── alumni.csv          # Dataset Alumni (Simulated)
│   └── scraper_log.txt         # Log Aktivitas Scraping (Observability)
│
├── src/
│   ├── scraper_job.py          # Service Utama (Hybrid Scraper)
│   └── generate_alumni.py      # Utility Generator Data Alumni
│
├── notebooks/                  # Eksperimen Data Science (EDA & Model)
├── README.md                   # Dokumentasi Proyek
└── requirements.txt            # Daftar Dependensi

```

---

## 🛠️ Instalasi & Cara Penggunaan

### 1. Clone Repository

```bash
git clone [https://github.com/USERNAME_GITHUB_KAMU/ub-linkops.git](https://github.com/USERNAME_GITHUB_KAMU/ub-linkops.git)
cd ub-linkops

```

### 2. Install Dependensi

Pastikan Python 3.9+ sudah terinstall, lalu jalankan:

```bash
pip install -r requirements.txt

```

*(Isi `requirements.txt`: selenium, pandas, webdriver-manager)*

### 3. Menjalankan Data Ingestion Service

Untuk memulai proses scraping lowongan kerja secara kontinu:

```bash
python src/scraper_job.py

```

*Script ini akan membuka browser (bisa di-set headless), mencari lowongan secara bergantian untuk berbagai jurusan, dan menyimpannya ke `data/raw/jobs_data.csv`.*

### 4. Meng-generate Data Alumni (Opsional)

Jika ingin memperbarui database alumni agar sinkron dengan data lowongan terbaru:

```bash
python src/generate_alumni.py

```

---

## 📊 Statistik Dataset (Saat Ini)

* **Total Lowongan Terkumpul:** 4.500+ Baris Data
* **Total Data Alumni:** 2.000+ Profil
* **Cakupan Domain:** IT, Engineering, Finance, Agriculture, Law, Creative.

---

## 👥 Tim Pengembang

Proyek ini dikembangkan oleh Mahasiswa **Universitas Brawijaya**:

1. **Muhammad Hasan Fadhlillah** (225150207111026)
2. **Muhammad Husain Fadhlillah** (225150207111027)

---

*Dibuat dengan ❤️ untuk kemajuan karier mahasiswa UB.*
