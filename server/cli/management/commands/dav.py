from django.core.management.base import BaseCommand

from cli import action, cli


class Command(BaseCommand):
    help = 'command line'

    def handle(self, *args, **options):
        action.show_info()
        cli.cli()
