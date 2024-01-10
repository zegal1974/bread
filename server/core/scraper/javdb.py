from core import config
from core.scraper.scraper import Scraper
# from api import config


class JavdbScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url_base = config.JAVDB_URL_BASE
        self.url_actors = f"{self.url_base}/actors/censored"
        self.url_actors_page = f"{self.url_base}/actors/censored?page=%i"
        self.url_actor = f"{self.url_base}/actors/%s"
        self.url_movie = f"{self.url_base}/m/%s"
