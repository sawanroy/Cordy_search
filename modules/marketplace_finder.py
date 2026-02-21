# modules/marketplace_finder.py

import json
import os
import re

from utils.search import search_duckduckgo
from utils.logger import log, set_stage


MARKETPLACE_DOMAINS = {
    "amazon": "amazon.in",
    "flipkart": "flipkart.com",
    "1mg": "1mg.com",
    "indiamart": "indiamart.com"
}


def normalize_amazon_url(url: str):
    """
    Extract and normalize Amazon product URL to:
    https://www.amazon.in/dp/ASIN
    """
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if asin_match:
        asin = asin_match.group(1)
        return f"https://www.amazon.in/dp/{asin}"
    return None


def find_marketplaces(company_name: str, company_path: str):

    set_stage("MARKETPLACE_DISCOVERY")

    marketplace_results = {}

    for name, domain in MARKETPLACE_DOMAINS.items():

        log(f"Searching {name} marketplace...")
        query = f"site:{domain} {company_name}"
        results = search_duckduckgo(query)

        filtered_links = []

        for r in results:
            href = r.get("href", "")

            if not href:
                continue

            # AMAZON SPECIAL HANDLING
            if name == "amazon":
                if "/dp/" in href:
                    normalized = normalize_amazon_url(href)
                    if normalized:
                        filtered_links.append(normalized)

            # FLIPKART BASIC FILTER
            elif name == "flipkart":
                if "/p/" in href:
                    cleaned = href.split("?")[0]
                    filtered_links.append(cleaned)

            # 1MG BASIC FILTER
            elif name == "1mg":
                if "/drugs/" in href or "/otc/" in href:
                    cleaned = href.split("?")[0]
                    filtered_links.append(cleaned)

            # INDIAMART BASIC FILTER
            elif name == "indiamart":
                cleaned = href.split("?")[0]
                filtered_links.append(cleaned)

        # Remove duplicates
        marketplace_results[name] = list(set(filtered_links))

    # -----------------------------------
    # Official Website Discovery
    # -----------------------------------
    set_stage("OFFICIAL_WEBSITE_DISCOVERY")

    website_query = f"{company_name} official website"
    website_results = search_duckduckgo(website_query)

    official_sites = []

    for r in website_results:
        href = r.get("href", "")

        if not href:
            continue

        # Exclude marketplace links
        if any(domain in href for domain in MARKETPLACE_DOMAINS.values()):
            continue

        official_sites.append(href)

    marketplace_results["official_website_candidates"] = official_sites[:3]

    # -----------------------------------
    # Save Results
    # -----------------------------------
    file_path = os.path.join(
        company_path,
        "marketplace",
        "marketplace_links.json"
    )

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(marketplace_results, f, indent=4)

    set_stage("MARKETPLACE_DONE")

    log("Marketplace discovery completed.")

    return marketplace_results