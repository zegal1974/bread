import os
import pathlib
import shutil
from api.models.models import Actor, Torrent
# import click
import ffmpeg

from api.utils import base


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
            prefix, number = base.get_code(filename)
            if prefix is not None and number is not None:
                code = base.code(prefix, number)
                if code not in results:
                    results[code] = []
                results[code].append(os.path.join(root, filename))
    return results


def ch_dir(path: str):
    """ Change to the direction, if direction, make the direction.
    """
    if not os.access(path, os.F_OK):
        os.makedirs(path)
    os.chdir(path)


def move_to_jav():
    pass


def get_actor_dir(actor: Actor) -> str:
    """ 返回 actress 的本地 video 保存目录
        :param actress:
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
                print(f"====Moving file {file} to {target} ...", nl=False)
                shutil.move(file, target)
                print("  OK.")
            except Exception:
                print('  ERR')
                continue


def collate(aid: str):
    """
    """
    actress = Actor.get(sid=aid)
    if actress is None:
        return
    collate_actor(actress)


def get_video_info(filename: str) -> dict:
    """ 获取视频文件的信息
        :param filename: 视频文件的文件名
    """
    results = {}
    info = ffmpeg.probe(filename)
    print(info)
    # logger.debug(info)
    if ('streams' not in info) or (len(info['streams']) == 0):
        # TODO: log the error.
        return {}
    results['codec'] = info['streams'][0].get('codec_name', None)
    # results['size'] = info['format']['size']
    results['bit_rate'] = info['streams'][0].get('bit_rate', 0)
    results['width'] = info['streams'][0].get('width', 0)
    results['height'] = info['streams'][0].get('height', 0)
    results['duration'] = info['streams'][0].get('duration', 0)

    return results


def main():
    pass


if __name__ == "__main__":
    pass
    # results = walk_dir('e:\\t')
    # print(results)
    # print(len(results))
    # for code, fts in results.items():
    #     print(code, fts)
    #     for ft in results[code]:
    #         if len(results[code][ft]) > 1:
    #             print(results[code][ft])

    # collate('qs6')
