import os
import pathlib
import shutil
import ffmpeg

from core import config
from core.models import Actor, Torrent, Video, Movie

from core.utils import base

WORD_RUNBKK = 'RUNBKK'

SOURCE_DIR = ['d:\\down', 'd:\\down1', 'd:\\downloads', 'e:\\data\\t']
MOVIE_DIR = 'e:\\data\\jp\\'
TORRENT_DIR = 'e:\\data\\torrents'
TORRENT_SOURCE_DIR = 'd:\\down\\'


def dir_torrent(torrent: Torrent) -> str:
    return os.path.join(TORRENT_DIR, torrent.hash, '.torrent')


def walk_dir(path: str) -> dict:
    results = {}
    for root, folders, filenames in os.walk(path):
        for filename in filenames:
            code = base.get_code(filename)
            if code is None:
                continue
            if code not in results:
                results[code] = [os.path.join(root, filename)]
            else:
                results[code].append(os.path.join(root, filename))
    return results


def ch_dir(path: str):
    """ Change to the direction, if direction, make the direction.
    """
    if not os.access(path, os.F_OK):
        os.makedirs(path)
    os.chdir(path)


def path_avatar(sid: str) -> str:
    return os.path.join(config.DIR_ACTOR_AVATARS, f"{sid}.jpg")


def path_thumbnail(code: str) -> str:
    pre, number = base.decode(code)
    return os.path.join(config.DIR_MOVIE_THUMBNAILS, pre, f"{code}_t.jpg")


def path_cover(code: str) -> str:
    pre, number = base.decode(code)
    return os.path.join(config.DIR_MOVIE_COVERS, pre, f"{code}_c.jpg")


def move_to_jav():
    pass


def get_actor_dir(actor: Actor) -> str:
    """ 返回 actress 的本地 video 保存目录
        :param actor:
    """
    return os.path.join(MOVIE_DIR, actor.name)


def copy_runbkk_torrent():
    """ 拷贝 runkbb 相关的种子文件到 torrent 目录
    """
    for path in os.listdir(TORRENT_SOURCE_DIR):
        if WORD_RUNBKK in path:
            file = list(pathlib.Path(
                TORRENT_SOURCE_DIR + path).glob("*.torrent"))
            if len(file) >= 1:
                if os.path.exists(os.path.join(TORRENT_DIR, base.get_basename(file[0].name))):
                    continue
                try:
                    shutil.copy(str(file[0]), TORRENT_DIR)
                finally:
                    continue


def collate_actor(actor: Actor):
    movies = actor.movies.all()
    target = get_actor_dir(actor)
    ch_dir(target)

    results = {}
    for path in SOURCE_DIR:
        results.update(walk_dir(path))

    for movie in movies:
        files = results.get(movie.code, [])
        for file in files:
            if os.path.exists(os.path.join(target, base.get_basename(file))):
                print(f"----- {file} is exists.")
                continue
            try:
                print(f"====Moving file {file} to {target} ...")
                shutil.move(file, target)
                print("  OK.")
            except Exception as e:
                print(f'  ERR, {e}')
                continue


def collate(aid: str):
    """
    """
    actress = Actor.objects.get(sid=aid)
    if actress is None:
        return
    collate_actor(actress)


def get_video_info(filename: str) -> dict:
    """ 获取视频文件的信息
        :param filename: 视频文件的文件名
    """
    results = {}
    info = ffmpeg.probe(filename)

    if ('streams' not in info) or (len(info['streams']) == 0):
        # TODO: log the error.
        return {}
    results['codec'] = info['streams'][0].get('codec_name', None)
    # results['size'] = info['format']['size']
    results['bit_rate'] = info['streams'][0].get('bit_rate', 0)
    results['width'] = info['streams'][0].get('width', 0)
    results['height'] = info['streams'][0].get('height', 0)
    results['duration'] = info['streams'][0].get('duration', 0)
    # print(results)
    return results


def refresh_videos():
    results = walk_dir(MOVIE_DIR)
    for code, files in results.items():
        for file in files:
            if base.is_movie(file):
                path = os.path.dirname(file)
                basename = os.path.basename(file)
                # print(file)
                info = get_video_info(file)

                code = base.get_code(basename)
                movie, m_created = Movie.objects.get_or_create(code=code)
                if m_created:
                    # TODO refresh movie.
                    pass
                info['movie'] = movie

                info['size'] = os.path.getsize(file)

                video, created = Video.objects.update_or_create(path=path, name=basename, defaults=info)


# def refresh_video():
#     file = 'e:\\data\\jp\\楓カレン\\ipx-596ch.mp4'
#     info = get_video_info(file)
#     return info


def refresh_avatars():
    for file in os.listdir(config.DIR_ACTOR_AVATARS):
        if base.is_image(file):
            name = base.get_basename(file)
            sid = name.split('.')[0]
            if Actor.objects.filter(sid=sid).exists():
                actor = Actor.objects.get(sid=sid)
                actor.avatar = file
                actor.save()
