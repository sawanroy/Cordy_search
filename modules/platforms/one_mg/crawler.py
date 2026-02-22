import time
import re
from modules.platforms.base_platform import BasePlatform
from utils.scraper import fetch_page
from utils.search import search_duckduckgo
from .parser import parse_product_page


class OneMgCrawler(BasePlatform):

    def __init__(self):
        super().__init__("one_mg")

    def crawl(self, company_name, limit=30):

        print("[1mg] Discovering products via DuckDuckGo")

        # Extract brand keyword safely
        brand_parts = company_name.lower().split()
        brand_parts = [p for p in brand_parts if p not in ["company", "pvt", "ltd", "limited"]]
        brand_keyword = brand_parts[0]

        query = f'site:1mg.com "{brand_keyword}"'
        results = search_duckduckgo(query)

        discovered_links = []

        for result in results:

            url = result.get("href") or result.get("url")

            if not url:
                continue

            # STRICT product-only URLs
            if (
                url.startswith("https://www.1mg.com/otc/")
                or url.startswith("https://www.1mg.com/drugs/")
            ):

                clean_url = url.split("?")[0]

                if clean_url not in discovered_links:
                    discovered_links.append(clean_url)

            if len(discovered_links) >= limit:
                break

        if not discovered_links:
            print("[1mg] No product links discovered.")
            return []

        products = []

        for link in discovered_links:

            print(f"[1mg] Scraping {link}")

            html = fetch_page(link)
            if not html:
                continue

            product_data = parse_product_page(html)

            product_name = product_data.get("name", "").lower()

            # WORD boundary match against product title only
            if not re.search(rf"\b{brand_keyword}\b", product_name):
                continue

            product_data["platform"] = "one_mg"
            product_data["url"] = link

            products.append(product_data)

            time.sleep(2)

        print(f"[1mg] Completed deep crawl. {len(products)} filtered products scraped.")

        return products