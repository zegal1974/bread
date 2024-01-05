import random
import time

from lxml import etree

from api.models.models import Movie, Actor, Publisher, Producer, Series, Magnet
from api.scraper.parse import parse_element, parse_tree
from api.scraper.scraper import Scraper
from api import config
from api.utils import db
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
        'fields': [
            {'name': 'thumb',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-frame"]/img/@src'},
            {'name': 'name',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/span/text()'},
            {'name': 'birthday',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "生日: ")]',
             'select': 'match("([0-9-]+)")'},
            {'name': 'age',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "年齡: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'height',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "身高: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'cups',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "罩杯: ")]',
             'select': 'normalize-space(substring-after(.,":"))'},
            {'name': 'bust',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "胸圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'waist',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "腰圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'hip',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "臀圍: ")]',
             'select': 'match("([0-9]+)")'},
            {'name': 'homeland',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "出生地: ")]',
             'select': 'normalize-space(substring-after(.,":"))'},
            {'name': 'hobiies',
             'xpath': '//div[@class="avatar-box"]//div[@class="photo-info"]/p[starts-with(text(), "愛好: ")]',
             'select': 'substring-after(.,":")'},
            {'name': 'summary',
             'xpath': '//a[@class="mypointer"]',
             'select': 'match("([0-9]+)")'},
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

    producer_css = {
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

    movie_magnets_css = {
        'xpath': '//tr',
        'fields': [
            {'name': 'link', 'xpath': 'td/a[rel="nofollow"][0]/@href'},
            {'name': 'size', 'xpath': 'td/a[rel="nofollow"][1]'},
            {'name': 'shared_on', 'xpath': 'td/a[rel="nofollow"][2]/text()'}
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

    def refresh_actor(self, sid: str, all_movies: bool = False) -> Actor:
        """ 刷新指定的 actor 信息和 movies 列表.
            :param sid: actor's sid
            :param all_movies: 是否扫描所有的 movies, 缺省为 False, 只刷新新增的

            :return data
        """
        content = self.get_html(self.url_actor(sid))
        doc = etree.HTML(content)
        adata = parse_element(doc, JavbusScraper.actor_css)
        actor = db.update_actor(adata)

        movies = parse_element(doc, JavbusScraper.movies_css)
        db.update_actor_movies(actor, movies)

        count = actor.movies.count()
        summary = adata['summary']

        if all_movies:
            max_page = summary // config.JAVBUS_COUNT_PRE_PAGE + 1
        else:
            max_page = (summary - count) // config.JAVBUS_COUNT_PRE_PAGE + 1

        self._refresh_actor_movies(actor, max_page)

        return actor

    def _refresh_actor_movies(self, actor: Actor, pages: int):
        for page in range(2, pages + 1):
            url = self.url_actor(actor.sid, page)
            content = self.get_html(url)
            doc = etree.HTML(content)

            movies = parse_element(doc, JavbusScraper.movies_css)
            db.update_actor_movies(actor, movies)

    def refresh_movie(self, code: str) -> dict:
        content = self.get_html(self.url_movie(code))
        doc = etree.HTML(content)
        movie = parse_element(doc, JavbusScraper.movie_css)

        self.refresh_movie_publisher(movie, doc)
        self.refresh_movie_producer(movie, doc)
        self.refresh_movie_series(movie, doc)
        self.refresh_movie_genres(movie, doc)

        movie.save()
        return movie

    def refresh_movie_publisher(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.publisher_css)
        publisher, created = Publisher.objects.update_or_create(sid=data['sid'], defaults=data)
        movie.publisher = publisher

    def refresh_movie_producer(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.producer_css)
        producer, created = Producer.objects.update_or_create(sid=data['sid'], defaults=data)
        movie.producer = Producer

    def refresh_movie_series(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.series_css)
        series, created = Series.objects.update_or_create(sid=data['sid'], defaults=data)
        movie.series = series

    def refresh_movie_genres(self, movie: Movie, doc):
        data = parse_tree(doc, JavbusScraper.genres_css)
        for g in data:
            genre, created = Series.objects.update_or_create(sid=g['sid'], defaults=g)
            if not movie.genres.exists(genre):
                movie.genres.add(genre)

    def refresh_movie_actors(self, movie: Movie, doc):
        data = parse_tree(doc, JavbusScraper.movie_actors_css)
        for a in data:
            actor, created = Series.objects.update_or_create(sid=a['sid'], defaults=a)
            if not movie.actors.exists(actor):
                movie.actors.add(actor)

    def refresh_movie_torrents(self, movie: Movie, gid: str):
        content = self.get_html(self.url_magnets(movie))
        doc = etree.HTML(content)
        data = parse_tree(doc, JavbusScraper.movie_magnets_css)
        for m in data:
            magnet, created = Magnet.objects.update_or_create(hash=m['hash'], defaults=m)
            if not movie.magnets.exists(magnet):
                movie.magnets.add(magnet)

    def refresh_actor_movies(self, actor: Actor, force=False):
        """ 刷新指定 actor 的 movies 的详细信息
            :param actor: 指定的 actor
            :param force: 是否刷新所有的 movies, 缺省是 False, 只刷新未刷新过的 movies
        """
        if force:
            movies = actor.movies.all()
        else:
            movies = actor.movies.filter(refreshed_at=None)

        for movie in movies:
            self.refresh_movie(movie.code)
            time.sleep(random.random())
