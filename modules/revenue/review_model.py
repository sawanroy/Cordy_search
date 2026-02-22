def extract_review_number(review_text):

    if not review_text:
        return 0

    import re
    match = re.search(r"[\d,]+", review_text)
    if not match:
        return 0

    return int(match.group().replace(",", ""))


def estimate_from_reviews(review_text):
    reviews = extract_review_number(review_text)
    return reviews * 20  # conservative multiplier