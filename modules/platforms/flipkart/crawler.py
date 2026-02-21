from modules.platforms.base_platform import BasePlatform


class FlipkartCrawler(BasePlatform):

    def __init__(self):
        super().__init__("flipkart")

    def crawl(self, company_name, limit=50):
        print(f"[Flipkart] Deep crawling up to {limit} products")
        return []