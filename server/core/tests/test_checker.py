from core.models import Movie
from core.utils import checker


def test_check_movie_names_remove_code():
    movie = Movie(code='ABC-001', name='ABC-001 movie name 1')
    checker.check_movie_names_remove_code(movie)
    assert movie.name == "movie name 1"
