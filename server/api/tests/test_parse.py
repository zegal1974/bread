from api.scraper.javbus import JavbusScraper
from api.scraper.parse import get_number, parse_element, parse_tree, parse_html
from lxml import etree


def test_get_id():
    pass


def test_get_number():
    assert get_number('123米') == 123
    assert get_number('T123米') == 123
    assert get_number('米') == 0


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
    with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        movie = parse_element(doc, JavbusScraper.movie_css)
        # print(movie)
        assert movie is not None
        assert movie['code'] == 'IPZZ-120'
        assert movie['published_on'] == '2023-10-06'
        assert movie['length'] == '120'


def test_parse_movie_productor():
    with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        productor = parse_element(doc, JavbusScraper.productor_css)
        # print(productor)
        assert productor is not None
        assert productor['sid'] == '1'


def test_parse_movie_publisher():
    with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        publisher = parse_element(doc, JavbusScraper.publisher_css)
        # print(publisher)
        assert publisher is not None
        assert publisher['sid'] == '5d'


def test_parse_movie_genres():
    with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        genres = parse_tree(doc, JavbusScraper.genres_css)
        print(genres)
        assert len(genres) == 7
        assert genres[0]['sid'] == '4o'


def test_parse_movie_actors():
    with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        actors = parse_tree(doc, JavbusScraper.movie_actors_css)
        assert len(actors) == 1
        assert actors[0]['sid'] == 'qs6'


def test_parse_actor_movies():
    with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        movies = parse_tree(doc, JavbusScraper.movies_css)
        # print(movies)
        assert len(movies) == 30
        assert movies[0]['code'] == 'IPZZ-120'


def test_parse_actor_info():
    with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        actor = parse_element(doc, JavbusScraper.actor_css)
        # print(actor)
        # assert actor[0]['sid'] == 'qs6'
        assert actor['age'] == '25'
        assert actor['cups'] == 'B'
        assert actor['bust'] == '80'
        assert actor['waist'] == '58'
        assert actor['summary'] == '140'


# def test_parse_movie_gid():
#     with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
#         doc = etree.HTML(f.read())
#         # actor = parse_tree(doc, JavbusScraper.actor_css)
#         find = etree.XPath(r'//script[re:match(text(), "var gid = ([0-9]+)")]',
#                            namespaces={"re": "http://exslt.org/regular-expressions"})
#         res = find(doc)
#         print(res, res.tag)
#         # print(actor)
#         # assert actor[0]['gid'] == 'qs6'
#         assert 1 == 2
