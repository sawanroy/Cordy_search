from urllib.parse import quote_plus

def build_search_url(company_name):
    query = quote_plus(company_name)
    return f"https://www.amazon.in/s?k={query}"