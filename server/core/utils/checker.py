import os
import shutil

import click

from core import config
# from peewee import prefetch

from core.models import Actor, Movie, Video, Torrent, Magnet
from core.utils import base
from core.utils.base import scan_path, get_basename
from core.utils.db import FIELDS_TORRENT
from core.utils.local import walk_dir, get_actor_dir, dir_torrent
from core.utils.magnet import get_torrent_info, get_magnet_hash

checkers = {'movie': [], 'actor': [], 'video': [], 'torrent': [], 'other': []}
CHECKER_CATEGORIES = ['actress', 'movie', 'video', 'torrent', 'other']

NAME_SPECIAL_PHRASE = [
    '【配信専用】', '★配信限定！', '【4K高画質】', '【スマホ推奨】', '【本編未収録スマホ専用スペシャルコンテンツ】',
    '【ファン限定】', '【閲覧注意】', '【※観覧注意】', '【※ヌキ過ぎ注意】', '【VR】', '【お得】']


def run_all_checkers():
    """ Run all checkers of registered.
    """
    run_actor_checkers()
    run_movie_checkers()
    run_video_checkers()
    run_torrent_checkers()
    run_other_checkers()


def run_movie_checkers():
    click.echo(f"Run the movie check-list. {len(checkers['movie'])} checkers.")
    if len(checkers['movie']) == 0:
        return
    movies = Movie.objects.all()
    for movie in movies:
        for check in checkers['movie']:
            if not check(movie):
                break


def run_actor_checkers():
    click.echo(f"Run the actor check-list. {len(checkers['actor'])} checkers.")
    if len(checkers['actor']) == 0:
        return
    actors = Actor.objects.all()
    for actor in actors:
        for check in checkers['actor']:
            check(actor)


def run_video_checkers():
    click.echo(f"Run the video check-list. {len(checkers['video'])} checkers.")
    if len(checkers['video']) == 0:
        return
    videos = Video.objects.all()
    for video in videos:
        for check in checkers['video']:
            if not check(video):
                break


def run_torrent_checkers():
    click.echo(f"Run the torrent check-list. {len(checkers['torrent'])} checkers.")
    if len(checkers['torrent']) == 0:
        return
    for check in checkers['torrent']:
        check()


def run_other_checkers():
    click.echo(f"Run the other check-list. {len(checkers['other'])} checkers.")
    if len(checkers['other']) == 0:
        return
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
    # for video in Video.objects.all():
    #     vs = Video.objects.filter(name=video.name)
    #     if len(vs) > 1:
    #         for v in vs[1:]:
    #             v.delete()
    pass


@checker('torrent')
def check_magnets():
    for magnet in Magnet.objects.all():
        magnet_link = magnet.link
        magnet_hash = magnet.hash.upper()
        if magnet_link is not None and magnet_hash is None:
            magnet.hash = get_magnet_hash(magnet_link)
            magnet.save()


@checker('torrent')
def refresh_torrents():
    print(">  check the all torrent files to record...")
    for root, folders, filenames in os.walk(config.DIR_TORRENTS):
        for fn in filenames:
            filename = os.path.join(root, fn)

            base.is_torrent(filename)
            info = get_torrent_info(filename)
            info['filename'] = filename
            print(info)
            Torrent.objects.update_or_create(hash=info['hash'], defaults=base.data_filter(info, FIELDS_TORRENT))


@checker('torrent')
def check_torrent_files():
    """ 逐个检查所有 `torrent` 是否已存在种子文件，并更新 `torrent` 记录
    """
    print(">  refresh all torrent files by downloaded...")
    # Torrent.objects.all().delete()
    for torrent_source in config.DIR_TORRENT_SOURCES:
        for root, folders, filenames in os.walk(torrent_source):
            for f in filenames:
                filename = os.path.join(root, f)
                check_torrent_file(filename)


def check_torrent_file(filename: str):
    if not base.is_torrent(filename):
        return False

    info = get_torrent_info(filename)
    info['hash'] = info['hash'].upper()

    if Magnet.objects.filter(hash__iexact=info['hash']).exists():
        dest = os.path.join(config.DIR_TORRENTS, info['hash'] + '.torrent')
        print(filename, info, dest)
        if os.path.exists(dest):
            os.remove(filename)
        else:
            shutil.copy(filename, dest)
            info['filename'] = dest
            Torrent.objects.update_or_create(hash=info['hash'], defaults=base.data_filter(info, FIELDS_TORRENT))
