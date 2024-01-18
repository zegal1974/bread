from core.scraper.javbus import JavbusScraper
from core.scraper.parse import parse_element, parse_tree
from lxml import etree


def test_get_id():
    pass


# def test_get_number():
#     assert get_number('123米') == 123
#     assert get_number('T123米') == 123
#     assert get_number('米') == 0

MHTML = """
<tr>
  <td><a href='http://test.com/abc'>ABC</a></td>
  <td><a href='http://test.com/abc1'>ABC1</a></td>
  <td><a href='http://test.com/abc2'>ABC2</a></td>
</tr>
<tr>
  <td><a href='http://test.com/def'>DEF</a></td>
  <td><a href='http://test.com/def1'>DEF1</a></td>
  <td><a href='http://test.com/def2'>DEF2</a></td>
</tr>
"""


def test_parse_tree_test():
    doc = etree.HTML(MHTML)
    node = doc.xpath('//tr')[0]
    print(node)
    print(node.xpath('./td/a[1]'))
    print(node.xpath('./td/a[last()]'))
    print(node.xpath('td/a[3]'))
    print(node.xpath('td/a[1]/@href'))
    link = node.xpath('/td/a[1]/@href')
    link1 = node.xpath('/td/a[2]/@href')
    name = node.xpath('/td/a[1]/text()')
    name1 = node.xpath('/td/a[2]/text()')
    name2 = node.xpath('/td/a[3]/text()')
    assert link == 'http://test.com/abc'
    assert link1 == 'http://test.com/abc1'
    assert name == 'ABC'
    assert name1 == 'ABC1'
    assert name2 == 'ABC2'
    assert 1 == 2


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
    with open('core/tests/files/magnets1.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        # magnets = parse_tree(doc, JavbusScraper.movie_magnets_css)
        # assert len(magnets) == 1
        # assert magnets[0]['sid'] == 'qs6'


def test_parse_movie_magnets1():
    with open('core/tests/files/magnets1.html', 'r', encoding='UTF-8') as f:
        doc = etree.HTML(f.read())
        tr = doc.xpath('//tr')[0]
        # print(tr.xpath('./td/a[1]'))
        print(tr.xpath('./td/a[@rel="nofollow"][1]'))
        link = tr.xpath('td/a[2]/text()')
        print(link)
        assert link == 'http://test.com/abc'


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
