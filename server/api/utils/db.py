import django
from django import apps

from api.models.models import Actor, Director, Genre, Movie, Producer, Publisher, Series
from api.utils import base

FIELDS_MOVIE = ('name', 'code', 'code_prefix', 'code_number', 'gid',
                'thumbnail', 'cover', 'length', 'rating', 'published_on')


def update_movie(data: dict) -> Movie:
    # TODO: add to handle when movie's key don't continue 'code':

    # print(ext.data_filter(data, FIELDS_MOVIE))
    movie, created = Movie.objects.update_or_create(
        code=data['code'], defaults=base.data_filter(data, FIELDS_MOVIE))

    if ('producer' in data) and ('sid' in data['producer']):
        producer, created = Producer.objects.update_or_create(
            sid=data['producer']['sid'], defaults=data['producer'])
        movie.producer = producer

    if ('series' in data) and ('sid' in data['series']):
        series, created = Series.objects.update_or_create(
            sid=data['series']['sid'], defaults=data['series'])
        movie.series = series

    if ('publisher' in data) and ('sid' in data['publisher']):
        publisher, created = Publisher.objects.update_or_create(
            sid=data['publisher']['sid'], defaults=data['publisher'])
        movie.publisher = publisher

    if ('director' in data) and ('sid' in data['director']):
        director, created = Director.objects.update_or_create(
            sid=data['director']['sid'], defaults=data['director'])
        movie.director = director

    if 'genres' in data:
        genres = movie.genres.all()
        for g in data['genres']:
            genre, b = Genre.objects.update_or_create(sid=g['sid'], defaults=g)
            if genre not in genres:
                movie.genres.add(genre)

    if 'actors' in data:
        actors = movie.actors.all()
        for a in data['actors']:
            actor, b = Actor.objects.update_or_create(sid=a['sid'], defaults=a)
            if actor not in actors:
                movie.actors.add(actor)

    movie.refreshed_at = django.utils.timezone.now()
    movie.save()

    return movie


def update_actor_movies(actor: Actor, data: tuple):
    for md in data:
        movie, created = Movie.objects.update_or_create(code=md['code'], defaults=md)
        if created:
            movie.actors.add(actor)
        else:
            if not movie.actors.exists(actor):
                movie.actors.add(actor)
        movie.save()


def update_actor(data: dict) -> Actor:
    """ Refresh the Actress by data.
        :param data: data of actress.
    """
    actor, created = Actor.objects.update_or_create(sid=data['sid'], defaults=data)
    return actor


def restore():
    # click.echo('Restoring the database ... ')
    tables = [i._meta.db_table for i in apps.get_models(
        include_auto_created=True)]
    print(tables)
    # for table in tables:
    #     click.echo('    %s ...' % table, nl=False)
    #     filename = 'db\\backup\\%s.json' % table
    #     if os.path.exists(filename):
    #         click.echo("restore the %s..." % table)
    #         with db.transaction():
    #             db[table].thaw(filename='db\\backup\\%s.json' %
    #                                     table, format='json', strict=True)
    #             # nested_txn.rollback()
    #     click.echo(' OK')
