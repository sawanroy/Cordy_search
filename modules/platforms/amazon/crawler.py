import time
import re
from modules.platforms.base_platform import BasePlatform
from utils.scraper import fetch_page
from .parser import parse_product_page


class AmazonCrawler(BasePlatform):

    def __init__(self):
        super().__init__("amazon")

    def crawl(self, company_name, limit=20):

        print("=== Starting AMAZON Deep Crawl ===")
        print(f"[Amazon] Deep crawling up to {limit} products")

        search_url = f"https://www.amazon.in/s?k={company_name.replace(' ', '+')}"
        html = fetch_page(search_url)

        if not html:
            print("[Amazon] ❌ Failed to load search page.")
            return []

        print(f"[Amazon Debug] Search page length: {len(html)}")

        html_lower = html.lower()

        # CAPTCHA detection
        if "captcha" in html_lower or "enter the characters you see below" in html_lower:
            print("[Amazon] 🚨 CAPTCHA detected. Amazon blocked the request.")
            return []

        # Soft block detection
        if len(html) < 5000:
            print("[Amazon] ⚠️ Page loaded but content too small. Likely blocked or redirected.")
            return []

        print("[Amazon] ✅ Search page loaded successfully.")

        # Extract ASIN links
        asin_links = set()

        for match in re.findall(r'/dp/([A-Z0-9]{10})', html):
            asin_links.add(f"https://www.amazon.in/dp/{match}")

            if len(asin_links) >= limit:
                break

        if not asin_links:
            print("[Amazon] ❌ No product links found. Possibly blocked.")
            return []

        products = []

        for link in asin_links:

            print(f"[Amazon] Scraping {link}")

            product_html = fetch_page(link)

            if not product_html:
                print("[Amazon] ⚠️ Failed to load product page.")
                continue

            product_html_lower = product_html.lower()

            if "captcha" in product_html_lower:
                print("[Amazon] 🚨 CAPTCHA triggered during product scraping.")
                break

            product_data = parse_product_page(product_html)

            if not product_data.get("name"):
                continue

            product_data["platform"] = "amazon"
            product_data["url"] = link

            products.append(product_data)

            time.sleep(3)  # Increased delay to reduce blocking

        print(f"[Amazon] Completed deep crawl. {len(products)} products scraped.")

        return products