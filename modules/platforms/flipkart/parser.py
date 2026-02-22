import re
from bs4 import BeautifulSoup


def parse_product_page(html):

    soup = BeautifulSoup(html, "html.parser")

    product = {
        "name": "",
        "price": "",
        "rating": "",
        "review_count": ""
    }

    # Title
    title = soup.find("span", {"class": "B_NuCI"})
    if title:
        product["name"] = title.get_text(strip=True)

    # Price
    price = soup.find("div", {"class": "_30jeq3"})
    if price:
        product["price"] = price.get_text(strip=True)

    # Rating
    rating = soup.find("div", {"class": "_3LWZlK"})
    if rating:
        product["rating"] = rating.get_text(strip=True)

    # Reviews
    review = soup.find("span", string=re.compile("Ratings"))
    if review:
        product["review_count"] = review.get_text(strip=True)

    return product