from modules.platforms.base_platform import BasePlatform


class OneMgCrawler(BasePlatform):

    def __init__(self):
        super().__init__("one_mg")

    def crawl(self, company_name, limit=30):
        print(f"[1mg] Deep crawling up to {limit} products")
        return []