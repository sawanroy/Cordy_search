import time
import random
import re
import requests
from modules.platforms.base_platform import BasePlatform
from .parser import parse_product_page


class FlipkartCrawler(BasePlatform):

    def __init__(self):
        super().__init__("flipkart")
        self.session = requests.Session()

    def get_headers(self):
        return {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            ]),
            "Accept-Language": "en-IN,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.flipkart.com/",
            "Connection": "keep-alive",
        }

    def fetch(self, url, retries=3):

        for attempt in range(retries):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=20
                )

                if response.status_code == 200:
                    return response.text

                print(f"[Flipkart] HTTP {response.status_code}")

            except Exception:
                print(f"[Flipkart] Attempt {attempt+1} failed")

            sleep_time = random.uniform(4, 8)
            print(f"[Flipkart] Retrying in {sleep_time:.2f}s")
            time.sleep(sleep_time)

        print("[Flipkart] Final failure.")
        return None

    def crawl(self, company_name, limit=20):

        print("=== Starting FLIPKART Deep Crawl ===")
        print(f"[Flipkart] Deep crawling up to {limit} products")

        search_url = f"https://www.flipkart.com/search?q={company_name.replace(' ', '+')}"
        html = self.fetch(search_url)

        if not html:
            print("[Flipkart] ❌ Failed to load search page.")
            return []

        if "captcha" in html.lower() or "blocked" in html.lower():
            print("[Flipkart] 🚨 Blocked or CAPTCHA detected.")
            return []

        print("[Flipkart] ✅ Search page loaded.")

        product_links = set()

        for match in re.findall(r'href="(/.+?/p/.+?)"', html):
            full_url = "https://www.flipkart.com" + match
            product_links.add(full_url)

            if len(product_links) >= limit:
                break

        if not product_links:
            print("[Flipkart] ❌ No product links found.")
            return []

        products = []

        for link in product_links:
            print(f"[Flipkart] Scraping {link}")

            product_html = self.fetch(link)
            if not product_html:
                continue

            product_data = parse_product_page(product_html)

            if not product_data.get("name"):
                continue

            product_data["platform"] = "flipkart"
            product_data["url"] = link

            products.append(product_data)

            time.sleep(random.uniform(3, 6))

        print(f"[Flipkart] Completed deep crawl. {len(products)} products scraped.")

        return products