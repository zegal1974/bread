from lxml import etree

from api.models.models import Movie, Actor
from api.scraper.parse import parse_element
from api.scraper.scraper import Scraper
from api import config
from api.utils.net import http_get


class JavbusScraper(Scraper):
    actors_css = {
        'xpath': '//div[@class="item"]/a[@class="avatar-box"]',
        'fields': [
            {'name': 'sid', 'xpath': '.', 'select': 'get_id()'},
            {'name': 'avatar', 'xpath': 'img/@src'},
            {'name': 'name', 'xpath': 'img/@title'},
        ]
    }

    # MAP_MOVIE_ATTRS = {
    #     "生日": "birthday", "年齡": "age", "身高": "height",
    #     "罩杯": "cups", "胸圍": "bust", "腰圍": "waist", '臀圍': 'hip',
    #     "出生地": "homeland", "愛好": "hobbies",
    # }
    # TODO:
    actor_css = {
        'xpath': '//div[@class="avatar-box"]',
        'fields': [
            {'name': 'thumb',
             'xpath': 'div[@class="photo-frame"]/img/@src'},
            {'name': 'name',
             'xpath': 'div[@class="photo-info"]/span/text()'},
            {'name': 'birthday',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "生日: ")]',
             'select': 'match("([0-9-]+)")'},
            {'name': 'age',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "年齡: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'height',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "身高: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'cups',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "罩杯: ")]',
             'select': 'normalize-space(substring-after(.,":"))'},
            {'name': 'bust',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "胸圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'waist',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "腰圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'hip',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "臀圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'homeland',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "出生地: ")]',
             'select': 'normalize-space(substring-after(.,":"))'},
            {'name': 'hobiies',
             'xpath': 'div[@class="photo-info"]/p[starts-with(text(), "愛好: ")]',
             'select': 'substring-after(.,":")'},
        ]
    }
    movies_css = {
        'xpath': '//div[@class="item"]/a[@class="movie-box"]',
        'fields': [
            {'name': 'code', 'xpath': '.', 'select': 'get_id()'},
            {'name': 'thumb', 'xpath': 'div/img/@src'},
            {'name': 'name', 'xpath': 'div/img/@title'},
        ]
    }

    movie_css = {
        'fields': [
            {'name': 'name', 'xpath': '//div[@class="container"]/h3/text()'},
            {'name': 'cover', 'xpath': '//div[@class="row movie"]//a/@href'},
            {'name': 'code',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"識別碼:")]/following::span/text()'},
            {'name': 'published_on',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"發行日期:")]/../text()'},
            {'name': 'length',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"長度:")]/..',
             'select': 'match("([0-9]+)")',
             'modifier': 'match("([0-9]+)")'},
            {'name': 'gid', 'xpath': '//script[contains(text(), "var gid = ")]',
             'select': 'match("var gid = ([0-9]+)")'}
        ],
    }

    publisher_css = {
        'fields': [
            {'name': 'sid',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"發行商:")]/following::a',
             'select': 'get_id()'},
            {'name': 'name',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"發行商:")]/following::a/text()'},
        ]
    }

    productor_css = {
        'fields': [
            {'name': 'sid',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"製作商:")]/following::a',
             'select': 'get_id()'},
            {'name': 'name',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"製作商:")]/following::a/text()'},
        ]
    }

    series_css = {
        'fields': [
            {'name': 'sid',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"系列:")]/following::a',
             'select': 'get_id()'},
            {'name': 'name',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"系列:")]/following::a/text()'},
        ]
    }

    genres_css = {
        'xpath': '//span[@class="genre"]',
        'fields': [
            {'name': 'sid',
             'xpath': 'label/a', 'select': 'get_id()'},
            {'name': 'name',
             'xpath': 'label/a/text()'},
        ]
    }

    movie_actors_css = {
        'xpath': '//span[@class="genre"]',
        'fields': [
            {'name': 'sid',
             'xpath': './a', 'select': 'get_id()'},
            {'name': 'name',
             'xpath': 'a/text()'},
        ]
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def url_actors(page=1) -> str:
        return config.JAVBUS_URL_ACTORS % page

    @staticmethod
    def url_actor(sid: str, page=1) -> str:
        """ Return the URL of the special actress.
            :param sid:  the sid of the actress
            :param page: the page of the actress
        """
        if page < 0:
            raise
        if page == 1:
            return config.JAVBUS_URL_ACTOR % sid
        else:
            return config.JAVBUS_URL_ACTOR_PAGE % (sid, page)

    @staticmethod
    def url_movie(code: str) -> str:
        """ Return the URL of the special movie.
            :param code:  the code of the movie
        """
        return config.JAVBUS_URL_MOVIE % code

    @staticmethod
    def url_magnets(movie: Movie):
        return config.JAVBUS_URL_MAGNETS % (movie.gid, movie.cover)

    def get_html(self, url: str) -> str | None:
        """
        TODO: add retry
        """
        req = http_get(url)
        if req is None or req.status_code == 404:
            return None
        return req.text

    def refresh_actor(self, sid: str, all_movies: bool = False) -> Actor | None:
        """ 刷新指定的 actor 信息和 movies 列表.
            :param sid: actor's sid
            :param all_movies: 是否扫描所有的 movies, 缺省为 False, 只刷新新增的

            :return actor
        """
        actor = None

        return actor

    def refresh_movie(self, code: str):
        content = self.get_html(self.url_movie(code))
        doc = etree.HTML(content)
        movie = parse_element(doc, JavbusScraper.movie_css['fields'])
        return movie
