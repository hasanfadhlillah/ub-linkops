# 🎓 UB-LinkOps: Intelligent Career Matcher & Alumni Network Analyzer

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow)
![Grafana](https://img.shields.io/badge/Grafana-Monitoring-F46800?style=for-the-badge&logo=grafana)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Deployment-FFD21E?style=for-the-badge&logo=huggingface)

> **Platform MLOps End-to-End yang menjembatani mahasiswa Universitas Brawijaya dengan dunia industri melalui Semantic Matching & Analisis Jejaring Alumni.**

---

## 📖 Latar Belakang Project
**UB-LinkOps** adalah proyek akhir mata kuliah **Machine Learning Operations (MLOps)** yang bertujuan untuk menyelesaikan masalah "mismatch" antara lulusan universitas dan kebutuhan industri.

Sistem ini menerapkan siklus **Closed-Loop MLOps** yang mengintegrasikan pengambilan data otomatis, pelatihan model berkelanjutan (*Continuous Training*), dan pemantauan performa (*Observability*).

Kami menggunakan pendekatan **Hybrid Intelligence**:
1.  **Semantic Matching (SBERT):** Mencocokkan konteks CV mahasiswa dengan lowongan kerja secara mendalam menggunakan *Sentence-BERT Transformers* (bukan sekadar keyword).
2.  **Alumni Network Booster:** Memberikan prioritas rekomendasi pada perusahaan yang memiliki rekam jejak mempekerjakan alumni Universitas Brawijaya.

---

## 🚀 Fitur Unggulan (Key Features)

### 🧠 Intelligent Core
* **SBERT Model:** Menggunakan model `all-MiniLM-L6-v2` untuk representasi vektor teks yang akurat.
* **Alumni Booster Algorithm:** Logika bisnis unik yang meningkatkan skor relevansi sebesar **15%** jika ditemukan alumni UB di perusahaan target.

### 🔄 MLOps Pipeline
* **Experiment Tracking:** Menggunakan **MLflow** untuk mencatat parameter model, metrik akurasi, dan durasi inferensi setiap kali training berjalan.
* **Data Versioning:** Menggunakan **DVC** untuk melacak perubahan dataset (raw vs processed).
* **Containerization:** Seluruh layanan (API, Frontend, Database, Monitoring) dibungkus dalam **Docker**.
* **CI/CD Automation:** Pipeline GitHub Actions untuk testing otomatis dan deployment ke Docker Hub.

### 👁️ Observability & Monitoring
* **Real-time Metrics:** Menggunakan **Prometheus** untuk mengumpulkan data latensi API dan throughput.
* **Grafana Dashboard:** Visualisasi kesehatan sistem, error rate (5xx), dan performa endpoint `/match`.

---

## 🌐 Link Demo (Live)

| Komponen | URL Akses | Deskripsi |
| :--- | :--- | :--- |
| **Frontend App** | [**ub-linkops.streamlit.app**](https://ub-linkops.streamlit.app/) | Antarmuka Mahasiswa (Upload CV) |
| **Backend API** | [**Hugging Face Space**](https://hasanfadhlillah01-ub-linkops-api.hf.space/docs) | Dokumentasi Swagger UI (API) |
| **Docker Hub** | [**hasanfadhlillah/ub-linkops**](https://hub.docker.com/r/hasanfadhlillah/ub-linkops) | Registry Image Container |

---

## 📂 Struktur Direktori

Project ini mengikuti standar struktur MLOps untuk menjamin *reproducibility*:

```text
ub-linkops/
├── .github/workflows/      # CI/CD Pipeline (GitHub Actions)
├── data/                   # Manajemen Data (Tracked by DVC)
│   ├── raw/                # Hasil scraping mentah
│   ├── processed/          # Data bersih siap training
│   └── external/           # Database Alumni UB
├── src/                    # Source Code Utama
│   ├── app/                # Backend API (FastAPI)
│   ├── frontend/           # UI Web (Streamlit)
│   ├── scraper/            # Hybrid Scraper (Selenium)
│   └── training/           # Pipeline Training Model
├── k8s/                    # Konfigurasi Kubernetes (Optional)
├── tests/                  # Unit Testing (pytest)
├── docker-compose.yml      # Orkestrasi Layanan Lokal
├── Dockerfile              # Blueprint Image API
├── Dockerfile.mlflow       # Blueprint Image MLflow (dengan driver db)
└── requirements.txt        # Dependensi Python

```

---

## 🛠️ Instalasi & Cara Menjalankan (Local)

### Metode 1: Menggunakan Docker (Rekomendasi)

Pastikan **Docker Desktop** sudah terinstall. Ini akan menjalankan seluruh ekosistem (API, Frontend, MLflow, Grafana, Prometheus, Postgres) secara bersamaan.

```bash
# 1. Clone Repository
git clone [https://github.com/hasanfadhlillah/ub-linkops.git](https://github.com/hasanfadhlillah/ub-linkops.git)
cd ub-linkops

# 2. Jalankan Docker Compose
docker compose up --build

```

**Akses Layanan Lokal:**

* **Frontend:** `http://localhost:8501`
* **API Docs:** `http://localhost:8000/docs`
* **MLflow UI:** `http://localhost:5000`
* **Grafana:** `http://localhost:3000` (User: admin/admin)

### Metode 2: Menjalankan Manual (Python)

Jika ingin menjalankan komponen secara terpisah:

```bash
# Install Dependensi
pip install -r requirements.txt

# 1. Menjalankan Training Model (Log ke Local MLflow)
python src/training/train.py

# 2. Menjalankan Backend API
uvicorn src.app.main:app --reload

# 3. Menjalankan Frontend Streamlit
streamlit run src/frontend/app.py

```

---

## 📊 Tech Stack

| Kategori | Teknologi |
| --- | --- |
| **Language** | Python 3.10 |
| **Web Framework** | FastAPI (Backend), Streamlit (Frontend) |
| **ML & NLP** | PyTorch, Sentence-Transformers (SBERT), Pandas |
| **Data Ops** | Selenium (Scraping), DVC (Versioning) |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **MLOps** | MLflow (Tracking), Hugging Face (Cloud Serving) |
| **Monitoring** | Prometheus, Grafana |

---

## 👥 Tim Pengembang

Proyek ini dikembangkan oleh Mahasiswa **Fakultas Ilmu Komputer, Universitas Brawijaya**:

1. **Muhammad Hasan Fadhlillah** (225150207111026)
2. **Muhammad Husain Fadhlillah** (225150207111027)

---

*Dibuat dengan ❤️ dan ☕ untuk Tugas Akhir MLOps.*
