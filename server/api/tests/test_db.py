from api.models.models import Movie, Actor
from api.utils import db


def test_save_movie_simple():
    actor = Actor.objects.create(name='actor1', sid='123')
    movies = ({'code': 'ABC-001', 'name': 'movie name 1', 'thumbnail': 'test1.png'},
              {'code': 'ABC-002', 'name': 'movie name 2', 'thumbnail': 'test2.png'},)

    db.update_actor_movies(actor, movies)

    assert Movie.objects.filter(code='ABC-001').exists()
    assert Movie.objects.count() == 2
