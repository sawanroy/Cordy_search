import re
from bs4 import BeautifulSoup


def extract_bought_last_month(html):
    match = re.search(r"(\d+[Kk]?)[\+ ]*\s*bought in past month", html)
    if not match:
        return None

    value = match.group(1).upper()

    if "K" in value:
        base = int(value.replace("K", "")) * 1000
    else:
        base = int(value)

    return base


def parse_product_page(html):

    soup = BeautifulSoup(html, "html.parser")

    product = {
        "name": "",
        "price": "",
        "rating": "",
        "review_count": "",
        "bought_last_month_raw": None
    }

    # Title
    title = soup.find(id="productTitle")
    if title:
        product["name"] = title.get_text(strip=True)

    # Price
    price = soup.find("span", {"class": "a-offscreen"})
    if price:
        product["price"] = price.get_text(strip=True)

    # Rating
    rating = soup.find("span", {"class": "a-icon-alt"})
    if rating:
        product["rating"] = rating.get_text(strip=True)

    # Review count
    review = soup.find(id="acrCustomerReviewText")
    if review:
        product["review_count"] = review.get_text(strip=True)

    # Bought last month badge
    badge = extract_bought_last_month(html)
    if badge:
        product["bought_last_month_raw"] = badge

    return product