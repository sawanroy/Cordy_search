# utils/scraper.py

import requests
from config import USER_AGENT, REQUEST_TIMEOUT
from utils.logger import log

def fetch_page(url: str):

    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        log(f"Failed to fetch {url}: {str(e)}", level="ERROR")
        return None