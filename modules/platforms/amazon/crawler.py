import time
import re
from urllib.parse import quote_plus
from modules.platforms.base_platform import BasePlatform
from utils.scraper import fetch_page
from .parser import parse_product_page


class AmazonCrawler(BasePlatform):

    def __init__(self):
        super().__init__("amazon")

    def build_search_url(self, company_name, page=1):
        query = quote_plus(company_name)
        return f"https://www.amazon.in/s?k={query}&page={page}"

    def extract_asins(self, html):
        return list(set(re.findall(r"/dp/([A-Z0-9]{10})", html)))

    def crawl(self, company_name, limit=50):

        print(f"[Amazon] Deep crawling up to {limit} products")

        discovered_asins = set()
        page = 1

        while len(discovered_asins) < limit and page <= 5:

            search_url = self.build_search_url(company_name, page)
            print(f"[Amazon] Fetching search page {page}")

            html = fetch_page(search_url)
            if not html:
                break

            asins = self.extract_asins(html)

            for asin in asins:
                if len(discovered_asins) >= limit:
                    break
                discovered_asins.add(asin)

            page += 1
            time.sleep(2)  # rate limit

        products = []

        for asin in list(discovered_asins)[:limit]:

            product_url = f"https://www.amazon.in/dp/{asin}"
            print(f"[Amazon] Scraping {product_url}")

            html = fetch_page(product_url)
            if not html:
                continue

            product_data = parse_product_page(html)
            product_data["platform"] = "amazon"
            product_data["url"] = product_url

            products.append(product_data)

            time.sleep(2)  # rate limit

        print(f"[Amazon] Completed deep crawl. {len(products)} products scraped.")

        return products