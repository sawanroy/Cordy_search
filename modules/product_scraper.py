# modules/product_scraper.py

import os
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from utils.scraper import fetch_page
from utils.logger import log


def extract_asins_from_html(html):
    return list(set(re.findall(r"/dp/([A-Z0-9]{10})", html)))


def scrape_amazon_product(url):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    product = {
        "url": url,
        "name": "",
        "price": "",
        "rating": "",
        "review_count": ""
    }

    title = soup.find(id="productTitle")
    if title:
        product["name"] = title.get_text(strip=True)

    price = soup.find("span", {"class": "a-offscreen"})
    if price:
        product["price"] = price.get_text(strip=True)

    rating = soup.find("span", {"class": "a-icon-alt"})
    if rating:
        product["rating"] = rating.get_text(strip=True)

    review = soup.find(id="acrCustomerReviewText")
    if review:
        product["review_count"] = review.get_text(strip=True)

    return product


def extract_amazon_products(company_name: str, company_path: str):

    log("Starting Amazon product extraction...")

    search_query = quote_plus(company_name)
    search_url = f"https://www.amazon.in/s?k={search_query}"

    log(f"Fetching Amazon search page: {search_url}")

    html = fetch_page(search_url)
    if not html:
        log("Failed to fetch Amazon search page.", level="ERROR")
        return []

    asins = extract_asins_from_html(html)

    if not asins:
        log("No ASINs found on search page.", level="WARNING")
        return []

    products = []

    for asin in asins[:5]:
        product_url = f"https://www.amazon.in/dp/{asin}"
        log(f"Scraping Amazon product: {product_url}")

        product_data = scrape_amazon_product(product_url)

        if product_data:
            products.append(product_data)

    file_path = os.path.join(company_path, "products", "amazon_products.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(products, f, indent=4)

    log("Amazon product extraction completed.")

    return products