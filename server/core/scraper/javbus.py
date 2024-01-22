import random
import time

import django
import requests
from lxml import etree
from requests import Timeout

from core.models.models import Movie, Actor, Publisher, Producer, Series, Magnet, Genre
from core.scraper.parse import parse_element, parse_tree
from core.scraper.scraper import Scraper
from core import config
from core.utils import db
from core.utils.magnet import get_magnet_hash, get_magnet_size


# from api.utils.net import http_get


class JavbusScraper(Scraper):
    actors_css = {
        'xpath': '//div[@class="item"]/a[@class="avatar-box"]',
        'fields': [
            {'name': 'sid', 'xpath': '.', 'select': 'get_id()'},
            {'name': 'avatar', 'xpath': 'img/@src'},
            {'name': 'name', 'xpath': 'img/@title'},
        ]
    }

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
            {'name': 'thumbnail', 'xpath': 'div/img/@src'},
            {'name': 'name', 'xpath': 'div/img/@title'},
        ]
    }

    movie_css = {
        'fields': [
            {'name': 'cover', 'xpath': '//div[@class="row movie"]//a', 'select': 'get_pic()'},
            {'name': 'name', 'xpath': '//div[@class="row movie"]//a/img/@title'},
            {'name': 'code',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"識別碼:")]/following::span/text()'},
            {'name': 'published_on',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"發行日期:")]/../text()'},
            {'name': 'length',
             'xpath': '//div[@class="row movie"]/div[2]/p/span[contains(text(),"長度:")]/..',
             'select': 'match("([0-9]+)")'},
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
            {'name': 'sid', 'xpath': 'label/a', 'select': 'get_id()'},
            {'name': 'name', 'xpath': 'label/a/text()'},
        ]
    }

    movie_actors_css = {
        'xpath': '//span[@class="genre"]',
        'fields': [
            {'name': 'sid', 'xpath': './a', 'select': 'get_id()'},
            {'name': 'name', 'xpath': 'a/text()'},
        ]
    }

    movie_magnets_css = {
        'xpath': '//tr',
        'fields': [
            {'name': 'link', 'xpath': './td[1]/a/@href'},
            {'name': 'name', 'xpath': './td[1]/a/text()'},
            {'name': 'size', 'xpath': './td[2]/a/text()'},
            {'name': 'shared_on', 'xpath': './td[3]/a/text()'}
        ]
    }

    headers = {"Referer": "https://www.dmmsee.lol/",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}

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
        try:
            # return requests.get(url, cookies=jar, headers=headers)
            req = requests.get(url, headers=JavbusScraper.headers)
        except Timeout as t:
            print(t)
        except ConnectionError as e:
            print(e)

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
        # print(content)
        doc = etree.HTML(content)
        adata = parse_element(doc, JavbusScraper.actor_css)
        adata['sid'] = sid
        actor = db.update_actor(adata)

        movies = parse_tree(doc, JavbusScraper.movies_css)
        db.update_actor_movies(actor, movies)

        count = actor.movies.count()
        summary = int(adata['summary'])

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
            # print(content)
            doc = etree.HTML(content)

            movies = parse_tree(doc, JavbusScraper.movies_css)
            db.update_actor_movies(actor, movies)

    def refresh_movie(self, code: str) -> Movie | None:
        content = self.get_html(self.url_movie(code))
        # print(content)
        if content is None:
            return None
        doc = etree.HTML(content)
        data = parse_element(doc, JavbusScraper.movie_css)
        movie, created = Movie.objects.update_or_create(code=code, defaults=data)

        self.refresh_movie_actors(movie, doc)
        self.refresh_movie_publisher(movie, doc)
        self.refresh_movie_producer(movie, doc)
        self.refresh_movie_series(movie, doc)
        self.refresh_movie_genres(movie, doc)
        self.refresh_movie_magnets(movie)

        movie.refreshed_at = django.utils.timezone.now()
        movie.save()
        return movie

    def refresh_movie_publisher(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.publisher_css)
        if 'sid' in data:
            publisher, created = Publisher.objects.update_or_create(sid=data['sid'], defaults=data)
            movie.publisher = publisher

    def refresh_movie_producer(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.producer_css)
        if 'sid' in data:
            producer, created = Producer.objects.update_or_create(sid=data['sid'], defaults=data)
            movie.producer = producer

    def refresh_movie_series(self, movie: Movie, doc):
        data = parse_element(doc, JavbusScraper.series_css)
        if 'sid' in data:
            series, created = Series.objects.update_or_create(sid=data['sid'], defaults=data)
            movie.series = series

    def refresh_movie_genres(self, movie: Movie, doc):
        data = parse_tree(doc, JavbusScraper.genres_css)
        for g in data:
            genre, created = Genre.objects.update_or_create(sid=g['sid'], defaults=g)
            movie.genres.add(genre)

    def refresh_movie_actors(self, movie: Movie, doc):
        data = parse_tree(doc, JavbusScraper.movie_actors_css)
        for a in data:
            actor, created = Actor.objects.update_or_create(sid=a['sid'], defaults=a)
            if not movie.actors.filter(id=actor.pk).exists():
                movie.actors.add(actor)

    def refresh_movie_magnets(self, movie: Movie):
        content = self.get_html(self.url_magnets(movie))
        magnets = self._parse_movie_magnets(movie, content)
        return magnets

    def _parse_movie_magnets(self, movie: Movie, content: str) -> list:
        doc = etree.HTML(content)
        data = parse_tree(doc, JavbusScraper.movie_magnets_css)
        magnets = []
        for m in data:
            m['size'] = get_magnet_size(m['size'])
            m['hash'] = get_magnet_hash(m['link'])
            m['movie'] = movie
            magnet, created = Magnet.objects.update_or_create(hash__iexact=m['hash'], defaults=m)
            if created:
                magnets.append(magnet)
        return magnets

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
