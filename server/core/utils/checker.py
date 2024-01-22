import os

import click

# from peewee import prefetch

from core.models import Actor, Movie, Video
from core.utils import base
from core.utils.local import walk_dir, get_actor_dir

# from pav.utils import ext
# from pav.utils.local import get_actress_dir, walk_dir, dir_torrent
# from pav.model import Movie, Actress, Video, Torrent

checkers = {'movie': [], 'actor': [], 'video': [], 'other': []}
CHECKER_CATEGORIES = ['actress', 'movie', 'video', 'other']

NAME_SPECIAL_PHRASE = [
    '【配信専用】', '★配信限定！', '【4K高画質】', '【スマホ推奨】', '【本編未収録スマホ専用スペシャルコンテンツ】',
    '【ファン限定】', '【閲覧注意】', '【※観覧注意】', '【※ヌキ過ぎ注意】', '【VR】', '【お得】']


def run_all_checkers():
    """ Run all checkers of registered.
    """
    click.echo("Run the actor check-list.")
    if len(checkers['actor']) > 0:
        run_actor_checkers()
    click.echo("Run the movie check-list.")
    if len(checkers['movie']) > 0:
        run_movie_checkers()
    click.echo("Run the video check-list.")
    if len(checkers['video']) > 0:
        run_video_checkers()
    click.echo("Run the other check-list.")
    if len(checkers['other']) > 0:
        # run_movie_checkers()
        pass


def run_movie_checkers():
    # actors = Actor.objects.filter(rating__gt=0)
    # ms = Movie.objects.all()
    # ma = Movie.actors()
    #
    # movies = prefetch(ms, ma, actors)
    # for movie in movies:
    #     for check in checkers['movie']:
    #         check(movie)
    movies = Movie.objects.all()
    for movie in movies:
        for check in checkers['movie']:
            if not check(movie):
                break


def run_actor_checkers():
    actors = Actor.objects.all()
    for actor in actors:
        for check in checkers['actor']:
            check(actor)


def run_video_checkers():
    videos = Video.objects.all()
    for video in videos:
        for check in checkers['video']:
            if not check(video):
                break


def run_other_checkers():
    for check in checkers['other']:
        if not check():
            break


def checker(category: str):
    def decorate(func):
        if category not in CHECKER_CATEGORIES:
            # TODO: raise Exception
            return
        checkers[category].append(func)
        return func

    return decorate


@checker('movie')
def check_movie_names_remove_code(movie: Movie):
    if movie.name.startswith(movie.code):
        movie.name = movie.name[len(movie.code):].strip()
        movie.save()
    return True


@checker('movie')
def check_movie_name_is_none(movie: Movie):
    if not movie.name:
        movie.delete()
        return False
    return True


@checker('movie')
def check_movie_names_remove_actress_name(movie: Movie):
    count = 0
    for actor in movie.actors.all():
        if movie.name[len(movie.name) - len(actor.name):] == actor.name:
            movie.name = movie.name[:-len(actor.name)].strip()
            count += 1
            movie.save()
    if count > 0:
        click.echo("Changed %s names of movie to remove actor name" % count)
    return True


@checker('movie')
def check_movie_names_remove_special(movie: Movie):
    """ 检查 `movie` 的名字，去除掉设定的前后缀
    """
    count = 0
    for phrase in NAME_SPECIAL_PHRASE:
        if movie.name[len(movie.name) - len(phrase):] == phrase:
            movie.name = movie.name[:-len(phrase)].strip()
            count += 1
            movie.save()
    if count > 0:
        click.echo("Changed %s names of movie to remove special phrases" % count)


# @checker('actor')
# def check_actor_videos(actor: Actor):
#     """  如果视频文件不存在，删除 `video` 记录
#        param actress: 被检查的 `video`
#     """
#     path = get_actor_dir(actor)
#     results = walk_dir(path)
#     for code, files in results.items():
#         movie = Movie.objects.get_or_none(code=code)
#         if movie:
#             for filename in files:
#                 if (base.is_movie(filename) and
#                     Video.objects.filter(name=filename).count() == 0):
#                     video = Video(movie=movie, name=filename, path=path)
#                     video.save()

@checker('video')
def check_video(video: Video):
    """  如果视频文件不存在，删除 `video` 记录
       param video: 被检查的 `video`
    """
    if not os.path.isfile(os.path.join(video.path, video.name)):
        video.delete()
        return False
    return True


@checker('video')
def check_video_definition(video: Video):
    pass


@checker('other')
def check_videos_duplicate():
    """ 检查 `video` 记录是否有重复的名字
    """
    for video in Video.select():
        vs = Video.select(Video.name == video.name)
        if len(vs) > 1:
            for v in vs[1:]:
                v.delete()

# @checker('other')
# def check_torrent_files():
#     """ 逐个检查所有 `torrent` 是否已存在种子文件，并更新 `torrent` 记录
#     """
#     for torrent in Torrent.select():
#         if torrent.filename is None:
#             filename = dir_torrent(torrent)
#             if os.path.isfile(filename):
#                 torrent.filename = filename
#                 torrent.save()
#         else:
#             if os.path.isfile(torrent.filename):
#                 torrent.filename = None
#                 torrent.save()
