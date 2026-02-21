# modules/entity_resolver.py

from utils.search import search_duckduckgo
from utils.logger import log


def resolve_entity(user_input: str):

    log("Resolving entity...")

    search_results = search_duckduckgo(user_input)

    if not search_results:
        log("Search returned no results.", level="ERROR")
        return {
            "input": user_input,
            "top_result": None,
            "search_results": []
        }

    # Try to find most relevant result
    official_result = None

    for result in search_results:
        title = result.get("title", "").lower()
        if user_input.lower().split()[0] in title:
            official_result = result
            break

    if not official_result:
        official_result = search_results[0]

    resolved_data = {
        "input": user_input,
        "top_result": official_result,
        "search_results": search_results
    }

    log("Entity resolution completed.")
    return resolved_data