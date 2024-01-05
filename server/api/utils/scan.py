from __future__ import annotations

from bs4 import BeautifulSoup

import random
import time
import datetime
import re

from api import config
from api.scraper.parse import get_id, get_number, get_pic
# import click

from api.utils.base import url_movie, url_actors, url_actor, url_magnets
from api.utils.net import http_get
# import logging

from api.models.models import Actor, Movie

from api.utils import base, db
# from api.models import tools

FILE_ACTOR = "db/backup/all_actresses.json"
MAX_PAGE_ACTORS = 980


# def refresh_all_actresses():
#     """ Refresh all Actresses' list, and save to json file. """
#     actresses = {}
#     for i in range(1, MAX_PAGE_ACTRESSES):
#         req = http_get(url_actresses(i))
#         if req is None or req.status_code == 404:
#             break

#         alist = _scan_actresses_list(req.text)
#         actresses = {**actresses, **alist}

#         delay = random.random()
#         time.sleep(delay)

#     ext.save_data(actresses, FILE_ACTRESS)
#     return actresses


def _scan_actors_list(content) -> dict:
    """ 解析一个 actor 的列表 HTML 页面内容，生成 actor 详细列表.
       :param content: HTML content of an actors' list
    """
    actors = {}
    doc = BeautifulSoup(content, 'lxml')
    links = doc.search("a.avatar-box.text-center")
    for link in links:
        actor = {}
        aid = get_id(link.attrs['href'])
        if aid is None:
            continue

        img = link.div.img
        actor['avatar'] = get_pic(img['src'])
        actor['name'] = img['title']
        actors[aid] = actor
    return actors


COUNT_PRE_PAGE = 30


def refresh_actor(sid: str, all_movies: bool = False) -> Actor | None:
    """ 刷新指定的 actor 信息和 movies 列表.
        :param sid: actor's sid
        :param all_movies: 是否扫描所有的 movies, 缺省为 False, 只刷新新增的

        :return actor
    """
    req = http_get(url_actor(sid))
    if req is None or req.status_code == 404:
        return None

    doc = BeautifulSoup(req.text, 'lxml')
    data = _scan_actor(doc)
    data['sid'] = sid
    data['refreshed_at'] = datetime.datetime.now()

    actor = db.refresh_actor(data)
    summary = _scan_movies_count(doc)
    count = Movie.objects.count()

    movies = _scan_movies_list(doc)

    if all_movies:
        max_page = summary // config.JAVBUS_COUNT_PRE_PAGE + 1
    else:
        max_page = (summary - count) // config.JAVBUS_COUNT_PRE_PAGE + 1

    movies = movies + _scan_actor_movies_list(sid, max_page)

    _update_actor_movies_list(actor, movies)

    return actor


def _scan_actor_movies_list(sid, pages=2) -> list:
    """ Scan the HTML document of movie, get the movie's gid.
       :param sid: 指定的 actor 的 sid.
       :pages: 最大页数，从第二页到指定页数进行扫描，获取 movie 列表信息.
    """
    movies = []
    for page in range(2, pages + 1):
        url = url_actor(sid, page)
        req = http_get(url)
        if req is None or req.status_code == 404:
            continue
        doc = BeautifulSoup(req.text, 'lxml')
        movies = movies + _scan_movies_list(doc)
    return movies


# TODO: move to action


def _update_actor_movies_list(actor: Actor, movies: list) -> Actor:
    """ Refresh the movies' list of the actor.
    """
    for movie in movies:
        mv, created = db.update_movie(movie)
        if created:
            mv.actors.add(actor)
        else:
            if not mv.actors.exists(actor):
                mv.actors.add(actor)
        mv.save()
    return actor


def refresh_actor_movies(actor: Actor, force=False):
    """ 刷新指定 actor 的 movies 的详细信息
        :param actor: 指定的 actor
        :param force: 是否刷新所有的 movies, 缺省是 False, 只刷新未刷新过的 movies
    """
    if force:
        movies = actor.movies.all()
    else:
        movies = actor.movies.filter(refreshed_at=None)

    for movie in movies:
        refresh_movie(movie)
        time.sleep(random.random())


MOVIE_ATTRS = ['name', 'thumbnail', 'published_on']

MAP_MOVIE_ATTRS = {
    "生日": "birthday", "年齡": "age", "身高": "height",
    "罩杯": "cups", "胸圍": "bust", "腰圍": "waist", '臀圍': 'hip',
    "出生地": "homeland", "愛好": "hobbies",
}


def _scan_movies_count(doc) -> int:
    """ Scan the HTML page of actress, get the count of movies.
        :param doc: BeautifulSoup document
        :return: return the count of movies.
    """
    a = doc.select("#resultshowmag")[0]
    match = re.search(r'([0-9]+)', a.text)
    if match:
        return int(match.group(1))
    return 0


def _scan_actor(doc) -> dict:
    """ Scan the HTML content of actor, get the actor information.
       :param doc: BeautifulSoup document
    """
    actor = {'name': doc.select(
        "#waterfall .avatar-box .photo-info span.pb10")[0].string}
    for p in doc.select("#waterfall .avatar-box .photo-info p"):
        v = p.string.split(':')
        if MAP_MOVIE_ATTRS[v[0]] and v[1]:
            text = v[1].strip()
            match = re.search(r'^([0-9]+)cm$', text)
            actor[MAP_MOVIE_ATTRS[v[0]]
                  ] = text if match is None else match.group(1)
    return actor


def _scan_movies_list(doc) -> list:
    """ Scan the HTML content of actor' movies list.
       :param doc: BeautifulSoup document
    """
    movies = []
    links = doc.select("#waterfall a.movie-box")
    for link in links:
        movie = {}
        img = link.select(".photo-frame img")[0]
        movie['thumbnail'] = img['src'].split('/')[-1]
        movie['name'] = img['title']
        date = link.select('.photo-info date')
        movie['code'] = date[0].string.strip().upper()
        movie['code_prefix'], movie['code_number'] = movie['code'].split('-')
        movie['published_on'] = date[1].string.strip()
        movies.append(movie)
    return movies


def refresh_movie(movie: Movie) -> Movie | None:
    """ 刷新 Movie 的详细信息
    """
    req = http_get(url_movie(movie.code))
    if req is None or req.status_code == 404:
        return None

    doc = BeautifulSoup(req.text, 'lxml')
    data = _scan_movie(doc)

    db.update_movie(data)

    magnets = refresh_magnets(movie)
    if magnets:
        movie.update_magnets(magnets)
    return movie


MAP_PROPERTIES = {
    "導演:": 'director', "製作商:": 'producer', "發行商:": 'publisher', "系列:": 'series'
}


def _scan_movie(doc) -> dict:
    """ Scan the HTML document of movie, get the movie's information.
       :param doc: BeautifulSoup document of the movie
    """
    movie = {}
    img = doc.select('.movie .screencap a.bigImage img')[0]
    movie['cover'] = get_pic(img['src'])
    movie['name'] = img['title']
    info = doc.select('.movie .info')[0]
    for span in info.select('p span.header'):
        prop = span.string.strip()
        if prop == "長度:":
            text = span.next_sibling
            movie['length'] = get_number(text.string.strip())
            continue
        if prop == "發行日期:":
            date = span.next_sibling.string.strip()
            movie['published_on'] = datetime.date(*map(int, date.split('-')))
            continue
        if prop in MAP_PROPERTIES:
            pp = MAP_PROPERTIES[prop]
            a = span.next_sibling.next_sibling
            ps = {'name': a.string.strip(), 'sid': get_id(a['href'])}
            movie[pp] = ps

    movie['gid'] = _scan_movie_gid(doc)
    movie['actors'] = _scan_movie_actors(doc)
    movie['genres'] = _scan_genres(doc)

    return movie


def _scan_movie_gid(doc) -> str | None:
    """ Scan the HTML document of movie, get the movie's gid.
       :param doc: BeautifulSoup document
    """
    for script in doc.select('script'):
        if script.string is None:
            continue
        match = re.search(r'var gid = ([0-9]+)', script.string)
        if match:
            gid = match.group(1)
            return gid
    return None


def _scan_movie_actors(doc) -> list:
    """ Scan the HTML document of the movie, get the actors list.
       :param doc: BeautifulSoup document of the movie
    """
    actors = []
    for a in doc.select('p span.genre > a'):
        actor = {'name': a.string.strip(), 'sid': get_id(a['href'])}
        actors.append(actor)
    return actors


def _scan_genres(doc) -> list:
    """ Scan the HTML document of the movie, get the genres list.
       :param doc: BeautifulSoup document of the movie
    """
    genres = []
    genre_toggle = doc.find(id='genre-toggle')

    p = genre_toggle.parent.next_sibling
    if p.name != 'p':
        p = p.next_sibling
    for a in p.select('span.genre a'):
        genre = {'sid': get_id(a['href']), 'name': a.string}
        genres.append(genre)
    return genres


def refresh_magnets(movie: Movie) -> list | None:
    """ Refresh the magnets of the movie
        :return: return the data of magnets
    """
    req = http_get(url_magnets(movie))
    if req is None or req.status_code != 200:
        return None

    doc = BeautifulSoup(req.text, 'lxml')
    data = _scan_magnets(doc)
    return data


def _scan_magnets(doc: BeautifulSoup) -> list:
    """ Scan the HTML document of the movie, get the magnets list.
       :param doc: BeautifulSoup document of the movie
    """
    results = []
    for tr in doc.select('tr'):
        magnet = {}
        cs = tr.select('td > a[rel="nofollow"]')
        magnet['link'] = cs[0]['href']
        # magnet['size'] = cs[1].string.strip()
        magnet['shared_on'] = cs[2].string.strip()
        results.append(magnet)
    return results


def main():
    # path = 'actor.html'
    # with open(path, 'r', encoding='UTF-8') as f:
    #     actor = scan_actor(f.read())
    #     print(actor)
    # actors = load_actors()
    # print(actors)
    # scan_all_actors()

    # refresh_movie('SSIS-646')
    movie = Movie.get_or_none(code='IPZZ-120')
    refresh_magnets(movie)


if __name__ == "__main__":
    main()
