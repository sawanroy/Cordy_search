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
    title = soup.find("h1")
    if title:
        product["name"] = title.get_text(strip=True)

    # Price
    price = soup.find("div", {"class": "PriceBoxPlanOption__price"})
    if price:
        product["price"] = price.get_text(strip=True)

    # Rating
    rating = soup.find("span", {"class": "RatingDisplay__rating-value"})
    if rating:
        product["rating"] = rating.get_text(strip=True)

    # Reviews
    review = soup.find("div", {"class": "RatingDisplay__rating-count"})
    if review:
        product["review_count"] = review.get_text(strip=True)

    return product