import streamlit as st
import requests
import pandas as pd
from pypdf import PdfReader # Import PdfReader

# --- KONFIGURASI ---
# Alamat Backend API
API_URL = "https://hasanfadhlillah01-ub-linkops-api.hf.space/match"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="UB-LinkOps Career Matcher",
    page_icon="🎓",
    layout="wide"
)

# --- HEADER & SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Logo_Universitas_Brawijaya.svg/2036px-Logo_Universitas_Brawijaya.svg.png", width=150)
    st.title("UB-LinkOps")
    st.markdown("---")
    st.write("**Tentang Aplikasi:**")
    st.info(
        """
        Sistem cerdas penghubung mahasiswa UB dengan dunia industri.
        Menggunakan **SBERT (AI)** dan **Alumni Network Booster**.
        """
    )
    st.write("Developed by:")
    st.text("Hasan & Husain (2025)")

# --- MAIN CONTENT ---
st.title("🎓 Intelligent Career Matcher")
st.markdown("### Temukan Pekerjaan yang Cocok dengan CV Kamu!")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Input Data Mahasiswa")
    with st.form("cv_form"):
        name = st.text_input("Nama Lengkap", placeholder="Contoh: Muhammad Hasan")
        major = st.selectbox("Jurusan / Fakultas", [
            "Teknik Informatika", "Sistem Informasi", "Teknik Komputer",
            "Akuntansi", "Manajemen", "Ekonomi Islam",
            "Teknik Sipil", "Teknik Mesin", "Teknik Elektro",
            "Ilmu Hukum", "Administrasi Publik", "Pertanian"
        ])
        
        # --- FITUR UPLOAD CV (PDF & TXT) ---
        # Sekarang support PDF dan TXT
        uploaded_file = st.file_uploader("Upload CV (Format PDF atau .txt)", type=['pdf', 'txt'])
        
        cv_text_input = ""
        if uploaded_file is not None:
            try:
                # Cek tipe file
                if uploaded_file.type == "application/pdf":
                    # Proses PDF
                    reader = PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    cv_text_input = text
                    st.success(f"✅ File PDF berhasil dibaca! ({len(reader.pages)} halaman)")
                else:
                    # Proses TXT (seperti sebelumnya)
                    cv_text_input = uploaded_file.read().decode("utf-8")
                    st.success("✅ File Text berhasil dibaca!")
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")

        # Text Area tetap ada untuk opsi Copy-Paste atau edit hasil upload
        # Value akan terisi otomatis jika file diupload
        cv_text = st.text_area("Isi / Edit CV:", value=cv_text_input, height=250, 
                               placeholder="Atau paste isi CV kamu di sini...")
        
        submit_btn = st.form_submit_button("🔍 Analisis Kecocokan Karir", type="primary")

with col2:
    st.subheader("🎯 Hasil Rekomendasi AI")
    
    if submit_btn:
        if not name or not cv_text:
            st.warning("Mohon lengkapi Nama dan Isi CV terlebih dahulu!")
        else:
            # Tampilkan Loading
            with st.spinner('Sedang mencocokkan vektor semantik & mengecek database alumni...'):
                try:
                    # Kirim Request ke Backend API
                    payload = {
                        "student_name": name,
                        "major": major,
                        "cv_text": cv_text
                    }
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        jobs = result['recommendations']
                        
                        if not jobs:
                            st.error("Belum ditemukan lowongan yang cocok. Coba perkaya deskripsi CV-mu!")
                        else:
                            st.success(f"Ditemukan {len(jobs)} lowongan potensial untuk {name}!")
                            
                            for job in jobs:
                                # Tampilan Card untuk setiap lowongan
                                with st.container():
                                    # Layout Card
                                    c1, c2 = st.columns([3, 1])
                                    
                                    with c1:
                                        # POIN 1: Title
                                        st.markdown(f"### {job['title']}")
                                        # POIN 2 & 3: Company & Location
                                        st.markdown(f"🏢 **{job['company']}** | 📍 {job.get('location', 'Indonesia')}")
                                    
                                    with c2:
                                        # POIN 4: Match Score (Final)
                                        score = job['match_score'] * 100
                                        st.metric("Kecocokan", f"{score:.1f}%")
                                    
                                    # POIN 5: Alumni Boost
                                    if job['alumni_boost']:
                                        st.markdown(
                                            """
                                            <div style='background-color: #FFF3CD; color: #856404; padding: 15px; border-radius: 8px; border-left: 5px solid #FFC107; margin-bottom: 10px;'>
                                                🚀 <b>ALUMNI BOOSTER AKTIF!</b><br>
                                                <small style='font-size: 0.9em;'>Ada Alumni UB di perusahaan ini! Skor relevansi dinaikkan <b>15%</b>.</small>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                    else:
                                        st.caption("Belum ada data alumni tersimpan di perusahaan ini.")

                                    # --- BAGIAN DETAIL TEKNIS ---
                                    with st.expander("🔍 Lihat Detail Teknis (Metadata)"):
                                        # POIN 6: Original Score (Sebelum Boost)
                                        st.write(f"**Original Semantic Score:** {job['original_score']:.4f}")
                                        # POIN 7: Job ID
                                        st.code(f"Job ID: {job['job_id']}")
                                        
                                    st.markdown("---")
                    else:
                        st.error(f"Gagal menghubungi server. Code: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi: {e}")
                    st.info("Pastikan API Backend (api-service) sudah berjalan!")