from core.scraper.javbus import JavbusScraper
from core.scraper.parse import parse_element, parse_tree
from lxml import etree
import xml.etree.ElementTree as ET


def test_get_id():
    pass


# def test_get_number():
#     assert get_number('123米') == 123
#     assert get_number('T123米') == 123
#     assert get_number('米') == 0


html = """
    <div class='item'>
      <a class='avatar-box' href='http://test.com/abc'>
        <img src='http://test.com/abc.jpg' title='ABC'></img>
      </a>
    </div>
    <div class='item'>
      <a class='avatar-box' href='http://test.com/def'>
        <img src='http://test.com/def.jpg' title='DEF'></img>
      </a>
    </div>
    """


def test_parse_tree():
    doc = etree.HTML(html)
    actors = parse_tree(doc, JavbusScraper.actors_css)
    assert len(actors) == 2


def test_parse_movie():
    with open('core/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        movie = parse_element(doc, JavbusScraper.movie_css)
        # print(movie)
        assert movie is not None
        assert movie['code'] == 'IPZZ-120'
        assert movie['published_on'] == '2023-10-06'
        assert movie['length'] == '120'
        assert movie['cover'] == '9zf8_b.jpg'
        assert movie['name'] == "テニス終わりの汗だく若妻つむぎさんに密着誘惑で痴女られた昼下がり 明里つむぎ"


def test_parse_movie_producer():
    with open('core/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        producer = parse_element(doc, JavbusScraper.producer_css)
        # print(productor)
        assert producer is not None
        assert producer['sid'] == '1'


def test_parse_movie_series():
    with open('core/tests/files/movie1.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        series = parse_element(doc, JavbusScraper.series_css)
        # print(productor)
        assert series is not None
        assert series['sid'] == 'u1h'


def test_parse_movie_publisher():
    with open('core/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        publisher = parse_element(doc, JavbusScraper.publisher_css)
        # print(publisher)
        assert publisher is not None
        assert publisher['sid'] == '5d'


def test_parse_movie_genres():
    with open('core/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        genres = parse_tree(doc, JavbusScraper.genres_css)
        print(genres)
        assert len(genres) == 7
        assert genres[0]['sid'] == '4o'


def test_parse_movie_actors():
    with open('core/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        actors = parse_tree(doc, JavbusScraper.movie_actors_css)
        assert len(actors) == 1
        assert actors[0]['sid'] == 'qs6'


def test_parse_movie_magnets():
    with open('core/tests/files/magnets.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        magnets = parse_tree(doc, JavbusScraper.movie_magnets_css)
        assert len(magnets) == 18
        assert magnets[0]['link'] == 'magnet:?xt=urn:btih:C51925A78553AE94F068A32F27EC67860A73AD5F&dn=MIAA-837_CH.HD'


def test_parse_actor_movies():
    with open('core/tests/files/star.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        movies = parse_tree(doc, JavbusScraper.movies_css)
        # print(movies)
        assert len(movies) == 30
        assert movies[0]['code'] == 'IPZZ-120'
        assert movies[0]['thumbnail'] == "/pics/thumb/9zf8.jpg"


def test_parse_actor_info():
    with open('core/tests/files/star.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        actor = parse_element(doc, JavbusScraper.actor_css)
        # print(actor)
        # assert actor[0]['sid'] == 'qs6'
        assert actor['age'] == '25'
        assert actor['cups'] == 'B'
        assert actor['bust'] == '80'
        assert actor['waist'] == '58'
        assert actor['summary'] == '140'
