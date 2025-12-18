import os
import time
import pandas as pd
import uuid
import random
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- KONFIGURASI ---
RAW_DATA_PATH = "data/raw/jobs_data.csv"
LOG_PATH = "data/scraper_log.txt"
SCRAPING_INTERVAL = 60

# List Keyword SUPER LENGKAP (Covering All UB Faculties)
SEARCH_KEYWORDS = [
    # --- TEKNOLOGI INFORMASI (FILKOM) ---
    "Software Engineer", "Frontend Developer", "Backend Developer", "Fullstack Developer",
    "Data Analyst", "Data Scientist", "UI/UX Designer", "IT Support", 
    "System Analyst", "DevOps Engineer", "Network Engineer", "Cyber Security",
    "Android Developer", "iOS Developer", "QA Engineer", "Product Manager",

    # --- EKONOMI & BISNIS (FEB & FIA) ---
    "Akuntansi", "Accounting Staff", "Tax Staff", "Auditor", 
    "Finance", "Banking", "Teller", "Customer Service",
    "Business Development", "Sales", "Marketing", "Digital Marketing",
    "Human Resources", "HRD", "Recruiter", "Admin", 
    "Sekretaris", "Public Relations", "Management Trainee", "Consultant",

    # --- TEKNIK (FT) ---
    "Teknik Sipil", "Civil Engineer", "Arsitek", "Drafter",
    "Teknik Mesin", "Mechanical Engineer", "Teknik Elektro", "Electrical Engineer",
    "Teknik Industri", "Industrial Engineer", "Project Manager", "Site Engineer",
    "HSE Officer", "K3", "Engineering Staff",

    # --- PERTANIAN & TEKNOLOGI PERTANIAN (FP, FTP, FAPET, FPIK) ---
    "Pertanian", "Agronomist", "Farm Manager", "Perkebunan",
    "Quality Control", "Quality Assurance", "Food Technology", "R&D Pangan",
    "Peternakan", "Fishery", "Aquaculture", "Lingkungan Hidup", "Staff Lapangan",

    # --- HUKUM & SOSIAL (FH, FISIP, FIB) ---
    "Legal Staff", "Legal Officer", "Hukum", "Notaris",
    "Content Creator", "Copywriter", "Social Media Specialist", "Journalist",
    "Translator", "Interpreter", "Guru", "Trainer", "Tutor",
    "Administrasi Publik", "Perpajakan"
]

# --- FUNGSI LOGGING ---
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"[{timestamp}] {message}"
    try:
        print(log_text)
    except UnicodeEncodeError:
        print(log_text.encode('ascii', 'ignore').decode('ascii'))
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_text + "\n")

# --- FALLBACK DATA (SAFETY NET) ---
def generate_fallback_data(keyword):
    """Generate 30 data dummy kalau scraping real gagal/diblokir."""
    titles = [f"{keyword} Staff", f"Senior {keyword}", f"{keyword} Intern", f"Head of {keyword}", f"Junior {keyword}"]
    companies = ["PT Mencari Cinta Sejati", "CV Maju Mundur", "PT Sumber Rejeki", "StartUp Gagal Bangkit", "PT Sejahtera Abadi"]
    locations = ["Jakarta", "Surabaya", "Malang", "Medan", "Bandung", "Bali"]
    
    dummy_jobs = []
    # Kita generate 30 data biar sama kayak kalau scraping berhasil
    for _ in range(30):
        dummy_jobs.append({
            "job_id": str(random.randint(10000000, 99999999)),
            "title": random.choice(titles),
            "company": random.choice(companies),
            "location": random.choice(locations),
            "description": f"Dibutuhkan segera {keyword} yang kompeten...",
            "skills": f"{keyword}, Microsoft Office, Teamwork",
            "posted_date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Fallback Data (Simulated)"
        })
    return dummy_jobs

# --- SELENIUM SETUP ---
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Comment kalau mau browsernya muncul
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

# --- CORE LOGIC (JOBSTREET SCRAPER) ---
def scrape_jobs():
    # 1. Pilih Keyword Acak
    current_keyword = random.choice(SEARCH_KEYWORDS)
    log_message(f"🚀 Service Bangun. Target Keyword: '{current_keyword}' di JobStreet Indo...")
    
    jobs = []
    # URL Search JobStreet Indonesia
    url = f"https://id.jobstreet.com/id/job-search/{current_keyword}-jobs/" 
    
    driver = None
    try:
        driver = setup_driver()
        driver.get(url)
        
        # Tunggu loading
        wait = WebDriverWait(driver, 20)
        
        # Cari elemen kartu lowongan (kadang pakai div role='listitem' atau article)
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[data-testid='job-card']")))
        
        if len(job_elements) == 0:
             # Coba selector alternatif kalau yang pertama gagal
             job_elements = driver.find_elements(By.CSS_SELECTOR, "article")

        log_message(f"🔎 Website JobStreet Terbuka. Ditemukan {len(job_elements)} lowongan.")

        count = 0
        for job in job_elements:
            if count >= 30: break 
            try:
                # Scroll biar kelihatan
                driver.execute_script("arguments[0].scrollIntoView();", job)
                
                try:
                    # Judul ada di a[data-automation='jobTitle']
                    title_el = job.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']")
                    title = title_el.text
                    link = title_el.get_attribute("href")
                    job_id = link.split("-")[-1].replace(".htm", "") if "-" in link else str(uuid.uuid4())[:8]
                except:
                    # Fallback ke h1
                    title_el = job.find_element(By.TAG_NAME, "h1")
                    title = title_el.text
                    link = "N/A"
                    job_id = str(uuid.uuid4())[:8]

                try:
                    # Company: a[data-automation='jobCompany']
                    company_el = job.find_element(By.CSS_SELECTOR, "a[data-automation='jobCompany']") 
                    company = company_el.text
                except:
                    company = "Confidential Company"

                try:
                    # Location: a[data-automation='jobLocation'] atau span
                    loc_el = job.find_element(By.CSS_SELECTOR, "a[data-automation='jobLocation']")
                    location = loc_el.text
                except:
                    location = "Indonesia"

                if title: # Hanya simpan kalau judul ketemu
                    jobs.append({
                        "job_id": job_id,
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": f"Real JobStreet Data for {current_keyword}. Apply at: {link}",
                        "skills": current_keyword, 
                        "posted_date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "JobStreet Indonesia (Real)"
                    })
                    count += 1
            except Exception as e:
                continue
        
        if len(jobs) > 0:
            log_message(f"✅ SUKSES! Berhasil menarik {len(jobs)} data REAL untuk '{current_keyword}'.")
        else:
            raise Exception("Tidak ada data yang bisa diekstrak (Selector mungkin berubah).")
        
    except Exception as e:
        log_message(f"⚠️ ERROR SCRAPING: {str(e)}")
        log_message(f"⚠️ Switch ke Fallback Data (Generate 30 data dummy).")
        jobs = generate_fallback_data(current_keyword)
        log_message(f"✅ Data Fallback ditambahkan ({len(jobs)} rows).")

    finally:
        if driver:
            driver.quit()

    return jobs

def save_to_datalake(new_jobs):
    df_new = pd.DataFrame(new_jobs)
    
    if os.path.exists(RAW_DATA_PATH):
        df_old = pd.read_csv(RAW_DATA_PATH)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new
        
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    df_final.to_csv(RAW_DATA_PATH, index=False)
    log_message(f"💾 Data Lake Updated! Total Data: {len(df_final)} baris.")

if __name__ == "__main__":
    log_message("🤖 UB-LinkOps Scraper Service STARTED (JobStreet Full Page Mode).")
    log_message(f"⏱️  Interval set to: {SCRAPING_INTERVAL} seconds.")
    log_message("------------------------------------------------")
    
    try:
        while True:
            data = scrape_jobs()
            save_to_datalake(data)
            
            log_message(f"💤 Service tidur selama {SCRAPING_INTERVAL} detik...")
            print("-" * 50)
            time.sleep(SCRAPING_INTERVAL)
            
    except KeyboardInterrupt:
        log_message("🛑 Service dihentikan manual.")
        sys.exit()