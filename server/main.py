import os
import sys
import django


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    django.setup()

    from cli import cli

    cli.cli()


if __name__ == "__main__":
    main()
