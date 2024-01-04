from django.core.management.base import BaseCommand

from api.scraper.javdb import JavdbScraper


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        # scraper = JavdbScraper()
        # ret = scraper.scan_all_actors()
        print("test")
