# modules/legal_identity.py

import json
import os
import re
from bs4 import BeautifulSoup

from utils.scraper import fetch_page
from utils.logger import log, set_stage


def extract_legal_identity(entity_data: dict, company_path: str):

    set_stage("LEGAL_FETCH_URL")

    top_result = entity_data.get("top_result", {})
    url = top_result.get("href")

    if not url:
        log("No URL found.", level="WARNING")
        return None

    log(f"Fetching URL: {url}")
    html_content = fetch_page(url)

    if not html_content:
        log("Failed to fetch page.", level="ERROR")
        return None

    set_stage("LEGAL_PARSE_HTML")

    soup = BeautifulSoup(html_content, "html.parser")

    structured_data = {
        "legal_name": "",
        "cin": "",
        "gst": "",
        "directors": [],
        "registered_address": "",
        "website": ""
    }

    # Extract page title
    if soup.title:
        structured_data["legal_name"] = soup.title.text.replace(" - Wikipedia", "").strip()

    # Extract infobox (Wikipedia structured table)
    infobox = soup.find("table", {"class": "infobox"})

    if infobox:
        rows = infobox.find_all("tr")

        for row in rows:
            header = row.find("th")
            value = row.find("td")

            if header and value:
                header_text = header.get_text(strip=True).lower()
                value_text = value.get_text(strip=True)

                if "key people" in header_text or "founder" in header_text:
                    structured_data["directors"].append(value_text)

                if "headquarters" in header_text:
                    structured_data["registered_address"] = value_text

                if "website" in header_text:
                    structured_data["website"] = value_text

    # Try regex for CIN pattern
    cin_match = re.search(r"[LU]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}", html_content)
    if cin_match:
        structured_data["cin"] = cin_match.group()

    # Try GST pattern
    gst_match = re.search(r"\d{2}[A-Z]{5}\d{4}[A-Z]\dZ\d", html_content)
    if gst_match:
        structured_data["gst"] = gst_match.group()

    file_path = os.path.join(company_path, "legal_identity.json")

    with open(file_path, "w") as f:
        json.dump(structured_data, f, indent=4)

    set_stage("LEGAL_DONE")

    log("Legal identity extracted (deterministic mode).")
    return structured_data