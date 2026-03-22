import re
import asyncio
import pandas as pd
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright

class ProfessionalEmailScraper:
    def __init__(self, base_url, max_pages=20):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.visited_urls = set()
        self.queue = [base_url]
        self.found_emails = set()

    async def scrape(self):
        async with async_playwright() as p:
            # Membuka browser Chromium
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            count = 0
            print(f"--- Memulai Scraping pada: {self.base_url} ---")
            
            while self.queue and count < self.max_pages:
                current_url = self.queue.pop(0)
                
                if current_url in self.visited_urls:
                    continue

                print(f"[{count+1}/{self.max_pages}] Memproses: {current_url}")
                try:
                    # Akses URL dengan timeout 30 detik
                    await page.goto(current_url, wait_until="networkidle", timeout=30000)
                    content = await page.content()
                    
                    # Regex untuk menangkap pola email standar
                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                    for email in emails:
                        if email not in self.found_emails:
                            print(f"   [+] Ditemukan: {email}")
                            self.found_emails.add(email)

                    # Mencari link internal untuk perayapan lebih dalam
                    links = await page.query_selector_all("a")
                    for link in links:
                        href = await link.get_attribute("href")
                        if href:
                            full_url = urljoin(current_url, href)
                            # Validasi agar tetap di domain yang sama
                            if self.domain in urlparse(full_url).netloc and full_url not in self.visited_urls:
                                self.queue.append(full_url)

                    self.visited_urls.add(current_url)
                    count += 1

                except Exception as e:
                    print(f"   [!] Gagal memproses {current_url}: {e}")

            await browser.close()
            self.save_results()

    def save_results(self):
        if not self.found_emails:
            print("\n[!] Tidak ada email yang ditemukan.")
            return

        df = pd.DataFrame(list(self.found_emails), columns=["Email Address"])
        filename = f"emails_{self.domain.replace('.', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"\n--- SELESAI ---")
        print(f"Total Email Unik: {len(self.found_emails)}")
        print(f"Data disimpan ke: {filename}")

# --- PENGATURAN TARGET ---
if __name__ == "__main__":
    # Masukkan URL target di sini
    TARGET_URL = "https://www.example.com" 
    # Batasi jumlah halaman agar tidak terlalu lama
    LIMIT_HALAMAN = 50 

    scraper = ProfessionalEmailScraper(TARGET_URL, max_pages=LIMIT_HALAMAN)
    asyncio.run(scraper.scrape())
