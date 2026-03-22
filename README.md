**AdvEmail-Scraper** adalah alat otomatisasi berbasis Python yang dirancang untuk melakukan perayapan (*crawling*) pada website publik guna mengekstraksi alamat email secara masif. Alat ini menggunakan mesin browser Playwright untuk memastikan email yang dimuat via JavaScript tetap tertangkap.

## ✨ Fitur Unggulan
- **JavaScript Rendering:** Mampu membaca konten dinamis (modern web apps).
- **Auto-Crawling:** Menelusuri seluruh sub-halaman dalam satu domain secara otomatis.
- **Filtering & Deduplication:** Hanya mengambil email unik dan tetap berada di domain target.
- **Export to CSV:** Menyimpan hasil secara rapi ke file Spreadsheet.

## 🛠️ Instalasi

1. **Clone Repositori**
   ```bash
   git clone [https://github.com/123tool/AdvEmail-Scraper.git](https://github.com/123tool/AdvEmail-Scraper.git)
   cd AdvEmail-Scraper

2. **Instal Library**
```bash
pip install -r requirements.txt
Instal Browser Engine
playwright install chromium
python scraper.py
