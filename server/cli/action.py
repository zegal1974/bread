import os

import click
import rich
from rich.table import Table

from core.jobs.download import download_avatar, download_thumbnail, download_cover
from core.models.models import Actor, Director, Genre, Magnet, Movie, Producer, Publisher, Series, Torrent, Video
from django.db.models import Q, Count

from core.scraper.javbus import JavbusScraper

from core.utils import base, checker, magnet
from core.utils.checker import checkers


def show_info():
    """ Show the summary information.
    """
    count_actors = Actor.objects.all().count()
    refreshed_actors = Actor.objects.filter(refreshed_at__isnull=False).count()
    rated_actors = Actor.objects.filter(rating__gt=0).count()
    count_movies = Movie.objects.count()
    refreshed_movies = Movie.objects.filter(refreshed_at__isnull=False).count()
    rated_movies = Movie.objects.filter(rating__gt=0).count()
    click.echo("Actors   : %3i/%3i/%-8i (rated/refreshed/total)" %
               (rated_actors, refreshed_actors, count_actors))
    click.echo("Movies   : %3i/%3i/%-8i (rated/refreshed/total)" %
               (rated_movies, refreshed_movies, count_movies))
    click.echo("Videos   : %-8i" % Video.objects.count())
    click.echo("Magnets  : %-8i" % Magnet.objects.count())
    click.echo("Torrents : %-8i" % Torrent.objects.count())
    click.echo("Genres   : %-8i" % Genre.objects.count())
    click.echo("Director : %-8i" % Director.objects.count())
    click.echo("Publisher: %-8i" % Publisher.objects.count())
    click.echo("Producer : %-8i" % Producer.objects.count())
    click.echo("Series   : %-8i" % Series.objects.count())


def show_actor_by_id(name: str):
    """ Show the actress information.
        :param name: the name or sid of actress.
    """
    actor = Actor.objects.get(Q(name=name) | Q(sid=name))
    if actor is None:
        click.echo("Can't find the actress, ID/NAME is %s." % name)
        return
    show_actor(actor)


def dv(value):
    if value:
        return value
    else:
        return '-'


def display_date(message, date, when_none=None):
    if date:
        click.echo("%s %i-%i-%i" %
                   (message, date.year, date.month, date.day))
    elif when_none:
        click.echo(when_none)


def _show_actor_info(actor):
    click.secho("%s " % actor.name, fg='yellow', nl=False)
    click.secho("%i   " % actor.rating, fg='red', nl=False)
    click.secho("%s" % base.url_actor(actor.sid))


def show_actor(actor: Actor):
    """ Show the actor information.
        :param actor: the actress
    """
    _show_actor_info(actor)

    click.echo("Height  %s,  Weight  %s" %
               (dv(actor.height), dv(actor.weight)))
    click.echo("Cups  %s,  Bust  %s,  Waist  %s,  Hip  %s" %
               (dv(actor.cups), dv(actor.bust), dv(actor.waist), dv(actor.hip)))
    display_date('Birthday : ', actor.birthday)
    click.echo("Homeland :  %s" % dv(actor.homeland))
    click.echo("Hobbies  :  %s" % dv(actor.hobbies))
    click.echo(
        "Has %i/%i movies,  " % (
            actor.movies.filter(refreshed_at__isnull=False).count(), actor.movies.count()),
        nl=False)
    display_date('refreshed at :', actor.refreshed_at, "Not refreshed yet.")


def show_actors():
    """ Show the Actresses table of set rating
    """
    count = Actor.objects.filter(Q(rating__gt=0) | Q(refreshed_at__isnull=False)).count()

    actors = (Actor.objects.filter(Q(rating__gt=0) | Q(refreshed_at__isnull=False))
              .values("id")
              .prefetch_related("movies")
              .annotate(count=Count('movies'))
              .order_by('-rating')
              .values_list('name', 'sid', 'rating', 'count', 'refreshed_at'))

    table = Table(title="%s Actresses have rated or refreshed." % count, box=None)
    table.add_column('Name')
    table.add_column('Link')
    table.add_column('Rating')
    table.add_column('Movies')
    table.add_column('Refreshed at')

    for actor in actors:
        table.add_row(actor[0], base.url_actor(actor[1]),
                      str(actor[2]),
                      str(actor[3]), base.date_to_str(actor[4]))

    rich.print(table)


def _movie_info(index, movie):
    """
    """
    name = movie.name
    name = name[:30] + '...' if len(name) > 30 else name

    return "%3i %9s %s" % (index + 1, movie.code, name)


def list_actor_movies(actor: Actor):
    """ Show the movies list of the specific actor
        :param actor: the specific actor
    """
    _show_actor_info(actor)

    count = actor.movies.count()
    movies = (Movie.objects.values('id')
              .prefetch_related("actors")
              .filter(actor__id=actor.id)
              .order_by("published_on")
              .annotate(count=Count("videos"))
              .values_list('code', 'count', 'published_on', 'name')
              )
    # print(movies)

    table = Table(title="%s Actors have rated or refreshed." % count, box=None)
    table.add_column('code')
    table.add_column('v')
    table.add_column('Published')
    table.add_column('Name', max_width=60)

    for index, movie in enumerate(movies):
        table.add_row(movie[0], str(movie[1]), str(movie[2]), movie[3])

    rich.print(table)


def show_movie_by_code(code: str):
    """ Show the information of movie, through the movie's code
        :param code: the movie's code
    """
    code = code.upper()
    movie = Movie.objects.get(code=code)
    if movie is None:
        click.echo("Can't find the movie, CODE is %s." % code)
        return
    show_movie(movie)


def show_movie(movie: Movie):
    """ Show the information of the specific movie
        :param movie: the specific movie
    """
    click.echo("%s" % movie.name)
    click.secho(movie.code, fg='yellow', nl=False)
    click.secho("  %i " % movie.rating, fg='red', nl=False)
    click.echo("  %s" % base.url_movie(movie.code))
    if movie.published_on:
        click.echo("published on %s" % movie.published_on)

    actors = movie.actors.all()
    _show_actors(actors)

    if movie.length:
        click.echo(f"Length    : {movie.length} minutes")
    if movie.publisher:
        click.echo(f"Publisher : {movie.publisher.name}({movie.publisher.sid})")
    if movie.producer:
        click.echo(f"Producer  : {movie.producer.name}({movie.producer.sid})")
    if movie.director:
        click.echo(f"Director  : {movie.director.name}({movie.director.sid})")

    genres = movie.genres.all()
    _show_genres(genres)

    click.echo("Has %s of magnets." % movie.magnets.count())

    _show_movie_videos(movie)


def _show_actors(actors):
    count = actors.count()
    if count > 1:
        click.echo("Actors    : %s" %
                   ', '.join(map(lambda actor: actor.name, actors)))
    elif count == 1:
        click.echo("Actor     : %s" % actors[0].name)


def _show_genres(genres):
    if len(genres) > 0:
        click.echo("Genres    : %s" %
                   ', '.join(map(lambda genre: genre.name, genres)))


def _show_movie_videos(movie: Movie):
    count = movie.videos.count()
    click.echo(f"Has {count} of videos.")

    if count > 0:
        table = Table(title="Has %s Videos." % count, box=None)
        table.add_column('codec')
        table.add_column('definition')
        table.add_column('path')
        table.add_column('name')

        for index, video in enumerate(movie.videos.all()):
            table.add_row(video.codec, video.definition, video.path, video.name)

        rich.print(table)


def refresh_actors():
    # count = Actor.objects.filter(Q(rating__gt=0) | Q(refreshed_at__isnull=False)).count()

    actors = Actor.objects.filter(rating__gt=0)

    for actor in actors:
        click.echo(f"{actor.name}({actor.sid}): ", nl=False)
        refresh_actor(actor.sid)
        click.echo('OK')


def refresh_actor(sid: str):
    scraper = JavbusScraper()
    actor = scraper.refresh_actor(sid)
    download_avatar(actor.sid)
    return actor


def refresh_movie(code: str):
    scraper = JavbusScraper()
    movie = scraper.refresh_movie(code)
    download_thumbnail(movie)
    download_cover(movie)
    # for m in movie.magnets.all():
    #     try:
    #         magnet.download_torrent_file(m.link)
    #     except Exception as e:
    #         print(e)
    #         continue
    return movie


def refresh_actor_movies(actor: Actor):
    scraper = JavbusScraper()
    scraper.refresh_actor_movies(actor)


def download_avatars():
    for actor in Actor.objects.all():
        download_avatar(actor.sid)
