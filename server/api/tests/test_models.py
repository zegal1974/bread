import datetime

from api.models.models import Actor, Genre, Movie
from api.utils import db


class TestActorModel:
    def setup_method(self):
        self.actor = Actor.objects.create(name='actor1', sid='123')

    def test_actror_create(self):
        assert self.actor.name == 'actor1'

    def test_actor_movie(self):
        m1 = Movie.objects.create(name='movie1', code='ABC-001')
        m1.actors.add(self.actor)
        m1.save()

        self.actor = Actor.objects.get(id=self.actor.id)
        assert self.actor.movies.all().count() == 1
        assert m1.actors.all().count() == 1
        assert self.actor.movies.all()[0] == m1
        assert m1.actors.all()[0] == self.actor

    def test_actror_get(self):
        a = Actor.objects.get(name='actor1')
        assert a.name == 'actor1'

    def test_actor_update_or_create_create(self):
        data = {'sid': '124', 'name': 'actor2'}
        actor, created = Actor.objects.update_or_create(
            sid=data['sid'], defaults=data)
        actor.save()

        assert created == True
        assert Actor.objects.all().count() == 2

    def test_actor_update_or_create_update(self):
        data = {'sid': '123', 'name': 'actor2'}
        actor, created = Actor.objects.update_or_create(
            sid=data['sid'], defaults=data)
        actor.save()

        assert created == False
        assert Actor.objects.all().count() == 1
        assert Actor.objects.first().name == 'actor2'

    # def test_refresh_actress(self):
    #     actress = Actor.refresh({'sid': 'id1', 'name': 'actress1'})
    #     assert actress.name == 'actress1'

    #     actress = Actor.refresh({'sid': 'id1', 'name': 'actress2', 'age': 20})
    #     assert actress.name == 'actress2'
    #     assert actress.age == 20


class TestMovieModel:
    def setup_method(self):
        self.movie = Movie.objects.create(name='movie', code='ABC-123')

    def test_movie_create(self):
        assert self.movie.name == 'movie'

    def test_movie_genre(self):
        g1 = Genre.objects.create(name='genre1', sid='123')
        self.movie.genres.add(g1)
        self.movie.save()

        assert g1.movies.count() == 1
        assert g1.movies.first() == self.movie

    def test_movie_update_datetime(self):
        self.movie.published_on = "2020-01-01"
        self.movie.save()
        self.movie.refresh_from_db()
        assert self.movie.published_on == datetime.date(2020, 1, 1)

    def test_movie_update_or_create_insert(self):
        data = {'name': 'movie2', 'code': 'ABC-001',
                'cover': 'test.jpg', 'length': '120',
                'rating': '90', 'published_on': '2023-11-11'}
        # Movie.objects.filter(code='ABC-001').update(**data)
        # m = Movie.objects.get(code='ABC-001')
        m, created = Movie.objects.update_or_create(
            code='ABC-001', defaults=data)
        assert created == True
        assert m.cover == 'test.jpg'

    def test_movie_update_or_create_update(self):
        data = {'name': 'movie2', 'code': 'ABC-123',
                'cover': 'test.jpg', 'length': '120',
                'rating': '90', 'published_on': '2023-11-11'}
        # Movie.objects.filter(code='ABC-001').update(**data)
        # m = Movie.objects.get(code='ABC-001')
        movie = db.update_movie(data)

        assert movie.cover == 'test.jpg'

    # def test_test(self):
    #     fields = self.movie._meta.get_fields()
    #     fs = list(map(lambda f: f.name, fields))
    #     print(fs)
    #     assert 1 == 2

    def test_movie_refresh_publisher(self):
        data = {'name': 'movie1', 'code': 'ABC-123',
                'publisher': {'sid': 'p1', 'name': 'publisher1'}}
        movie = db.update_movie(data)
        # movie = Movie.objects.get(Movie.code == 'ABC-123')
        assert movie.publisher is not None
        assert movie.publisher.name == 'publisher1'

    def test_movie_refresh_producer(self):
        data = {'name': 'movie1', 'code': 'ABC-001',
                'producer': {'sid': 'p1', 'name': 'producer1'}}
        movie = db.update_movie(data)
        # movie = Movie.get_or_none(Movie.code == 'ABC-001')
        assert movie.producer is not None
        assert movie.producer.name == 'producer1'

    def test_movie_refresh_director(self):
        data = {'name': 'movie1', 'code': 'ABC-001',
                'director': {'sid': 'd1', 'name': 'director1'}}
        movie = db.update_movie(data)
        # movie = Movie.get_or_none(Movie.code == 'ABC-001')
        assert movie.director is not None
        assert movie.director.name == 'director1'

    def test_movie_refresh_genres(self):
        data = {'name': 'movie1', 'code': 'ABC-001',
                'genres': [{'sid': 'g1', 'name': 'genre1'}, {'sid': 'g2', 'name': 'genre2'}]}
        movie = db.update_movie(data)

        assert Genre.objects.all().count() == 2
        assert movie.genres.count() == 2
        assert movie.genres.all()[0].sid == 'g1'
