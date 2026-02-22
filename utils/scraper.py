import requests
import random
import time


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118 Safari/537.36",
]


def fetch_page(url, retries=3):

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
        "Connection": "keep-alive",
    }

    for attempt in range(retries):

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"[Scraper] Attempt {attempt+1} failed for {url}")

            if attempt < retries - 1:
                sleep_time = random.uniform(3, 7)
                print(f"[Scraper] Retrying in {sleep_time:.2f} sec")
                time.sleep(sleep_time)
            else:
                print(f"[Scraper] Final failure for {url}")
                return None