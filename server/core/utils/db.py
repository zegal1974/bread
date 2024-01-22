import django
from django.apps import apps

from core.models.models import Actor, Director, Genre, Movie, Producer, Publisher, Series
from core.utils import base
from core.utils.base import load_data, save_data

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
        movie.actors.add(actor)
        movie.save()


def update_actor(data: dict) -> Actor:
    """ Refresh the Actress by data.
        :param data: data of actress.
    """
    actor, created = Actor.objects.update_or_create(sid=data['sid'], defaults=data)
    return actor


tables = ['Actor', 'Director', 'Genre', 'Producer', 'Publisher', 'Series', 'Movie', 'Magnet', 'ActorsMovies',
          'GenresMovies']


def db_backup():
    for table in tables:
        model = apps.get_model('core.%s' % table)
        print(table, model.objects.count())
        instances = model.objects.all()
        save_data(instances, 'tmp/' + table.lower() + '.json')


def db_restore():
    import warnings
    warnings.filterwarnings("ignore")

    for table in tables:
        data = load_data('tmp/' + table.lower() + '.json')
        model = apps.get_model('core.%s' % table)
        print(table)
        instances = [model(**item) for item in data]
        model.objects.bulk_create(instances)
        print(table, model.objects.count())
