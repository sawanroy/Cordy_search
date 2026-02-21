class BasePlatform:

    def __init__(self, name):
        self.name = name

    def search(self, company_name):
        raise NotImplementedError

    def extract_links(self, html):
        raise NotImplementedError

    def parse_product(self, html):
        raise NotImplementedError

    def crawl(self, company_name, limit=50):
        raise NotImplementedError