import os
import re
from django import apps
from django.core.management.base import BaseCommand

from playhouse.dataset import DataSet

from api.models.models import Actor


def get_tables():
    ret = []
    tables = [i._meta.db_table for i in apps.apps.get_models(
        include_auto_created=True)]
    for table in tables:
        m = re.search(r'^api_([a-z]+)$', table)
        if m:
            ret.append(m.group(1))
    return ret


class Command(BaseCommand):
    help = 'restore'

    def handle(self, *args, **options):
        print('Restoring the database ... ')
        db = DataSet('sqlite:///database.sqlite3')

        tables = get_tables()
        for table in tables:
            print('    %s ...' % table)
            filename = 'tmp\\%s.json' % table
            if not os.path.exists(filename):
                continue
            print("    restore the %s..." % table)
            with db.transaction():
                db['api_'+table].thaw(filename=filename,
                                      format='json', strict=True)
