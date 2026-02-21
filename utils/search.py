# utils/search.py

from ddgs import DDGS
from config import DUCKDUCKGO_MAX_RESULTS
from utils.logger import log

def search_duckduckgo(query: str):

    log(f"Searching DuckDuckGo for: {query}")

    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=DUCKDUCKGO_MAX_RESULTS):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body")
                })
    except Exception as e:
        log(f"Search error: {str(e)}", level="ERROR")
        return []

    if not results:
        log("No search results found.", level="WARNING")

    return results