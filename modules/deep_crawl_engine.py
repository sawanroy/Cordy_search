import os
import json
from modules.platforms.amazon import AmazonCrawler
from modules.platforms.flipkart import FlipkartCrawler
from modules.platforms.one_mg import OneMgCrawler


class DeepCrawlEngine:

    def __init__(self):
        self.platforms = [
            AmazonCrawler(),
            FlipkartCrawler(),
            OneMgCrawler()
        ]

    def run(self, company_name, company_path):

        all_results = {}

        for platform in self.platforms:

            print(f"\n=== Starting {platform.name.upper()} Deep Crawl ===")

            results = platform.crawl(company_name, limit=50)

            # Create platform-specific product folder
            platform_folder = os.path.join(
                company_path,
                "products",
                platform.name
            )
            os.makedirs(platform_folder, exist_ok=True)

            file_path = os.path.join(
                platform_folder,
                f"{platform.name}_products.json"
            )

            with open(file_path, "w") as f:
                json.dump(results, f, indent=4)

            all_results[platform.name] = results

            print(f"[{platform.name}] Saved {len(results)} products.")

        return all_results