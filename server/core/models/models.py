from django.db import models
# from django.db.models import Model

from django.db.models import ForeignKey, TextField, Model, CharField, IntegerField, DateField, DateTimeField, \
    SET_NULL, FloatField, ManyToManyField


class Actor(Model):
    sid = CharField(max_length=10, db_index=True, default='', unique=True)
    name = CharField(max_length=100, db_index=True)
    gender = IntegerField(default=2, null=True)
    age = IntegerField(default=0, null=True)
    avatar = CharField(max_length=200, null=True)
    birthday = DateField(null=True)
    height = IntegerField(null=True)
    weight = IntegerField(null=True)
    cups = CharField(max_length=5, null=True)
    bust = IntegerField(null=True)
    waist = IntegerField(null=True)
    hip = IntegerField(null=True)
    homeland = CharField(max_length=100, null=True)
    hobbies = CharField(max_length=100, null=True)
    rating = IntegerField(null=True)
    refreshed_at = DateTimeField(null=True)
    status = IntegerField(default=0, null=True)
    description = TextField(default='', null=True)

    current = ForeignKey(
        'self', null=True, related_name='previous', on_delete=SET_NULL)

    movies = ManyToManyField(
        'Movie', through='ActorsMovies', through_fields=("actor", "movie"))

    # class Meta:
    #     indexes = [
    #         Index(fields=['name']),
    #         Index(fields=['sid'])
    #     ]


class Director(Model):
    sid = CharField(max_length=10, db_index=True, unique=True)
    name = CharField(max_length=100, db_index=True, unique=True)
    description = TextField(default='', null=True)


class Genre(Model):
    sid = CharField(max_length=10, db_index=True, unique=True)
    name = CharField(max_length=100, db_index=True)
    description = TextField(default='', null=True)

    movies = ManyToManyField(
        'Movie', through="GenresMovies", through_fields=('genre', 'movie'))


class Producer(Model):
    sid = CharField(max_length=10, db_index=True, unique=True)
    name = CharField(max_length=100, db_index=True, unique=True)
    alias = CharField(max_length=100, null=True)
    rating = IntegerField(null=True)
    description = TextField(null=True)


class Publisher(Model):
    """ 发行商
    """
    sid = CharField(max_length=10, db_index=True, unique=True)
    name = CharField(max_length=100, db_index=True, unique=True)
    alias = CharField(max_length=100, null=True)
    parent = ForeignKey('self', null=True,
                        related_name='children', on_delete=SET_NULL)
    rating = IntegerField(null=True)
    description = TextField(null=True)


class Series(Model):
    sid = CharField(max_length=10, db_index=True, unique=True)
    name = CharField(max_length=100, db_index=True, unique=True)
    description = TextField(default='', null=True)


class Movie(Model):
    name = CharField(max_length=100, db_index=True)
    code = CharField(max_length=10, db_index=True, unique=True)
    code_prefix = CharField(max_length=10, null=True)
    code_number = CharField(max_length=10, null=True)
    gid = IntegerField(null=True)
    thumbnail = CharField(max_length=100, null=True)
    cover = CharField(max_length=100, null=True)
    length = IntegerField(null=True)
    series = ForeignKey(Series, null=True,
                        related_name='movies', on_delete=SET_NULL)
    director = ForeignKey(Director, null=True,
                          related_name='movies', on_delete=SET_NULL)
    producer = ForeignKey(Producer, null=True,
                          related_name='movies', on_delete=SET_NULL)
    publisher = ForeignKey(Publisher, null=True,
                           related_name='movies', on_delete=SET_NULL)
    published_on = DateField(null=True)
    rating = IntegerField(default=0, null=True)
    refreshed_at = DateTimeField(null=True)
    description = TextField(default='', null=True)

    actors = ManyToManyField(
        'Actor', through='ActorsMovies', through_fields=("movie", "actor"))
    genres = ManyToManyField(
        'Genre', through="GenresMovies", through_fields=('movie', 'genre'))


class ActorsMovies(Model):
    actor = ForeignKey(Actor, on_delete=models.CASCADE)
    movie = ForeignKey(Movie, on_delete=models.CASCADE)


class GenresMovies(Model):
    genre = ForeignKey(Genre, on_delete=models.CASCADE)
    movie = ForeignKey(Movie, on_delete=models.CASCADE)


class Video(Model):
    movie = ForeignKey(
        Movie, null=True, related_name='videos', on_delete=SET_NULL)
    name = CharField(max_length=100)
    path = CharField(max_length=100)
    md5 = CharField(max_length=100, null=True)
    codec = CharField(max_length=100, null=True)
    width = IntegerField(default=0)
    height = IntegerField(default=0)
    duration = FloatField(default=0)
    size = IntegerField(default=0)
    bit_rate = IntegerField(default=0)


class Magnet(Model):
    movie = ForeignKey(
        Movie, null=True, related_name='magnets', on_delete=SET_NULL)
    link = CharField(max_length=100, null=True)
    hash = CharField(max_length=100, null=True)
    size = IntegerField(null=True)
    language = CharField(max_length=100, null=True)
    definition = CharField(max_length=100, null=True)
    shared_on = DateField(null=True)


class Torrent(Model):
    hash = CharField(max_length=100, db_index=True, unique=True)
    filename = CharField(max_length=100, null=True)
    name = CharField(max_length=100, null=True)
    number = IntegerField(null=True)
    size = IntegerField(null=True)
    published_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)

    # movies = ManyToManyField(Movie, backref='torrents')
