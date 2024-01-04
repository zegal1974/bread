

import os
import sys
import django
from django.conf import settings
from django.core.management.base import BaseCommand


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    django.setup()
    # settings.configure()

    # print(django.apps)

    from cli import cli

    cli.cli()


if __name__ == "__main__":
    main()
