import json
import os
import re
from typing import Tuple

from core.models.models import Movie

URL_BASE = "https://www.dmmsee.lol"
URL_ACTORS = f"{URL_BASE}/actresses"
URL_ACTOR = f"{URL_BASE}/star/%s"
URL_ACTOR_PAGE = f"{URL_BASE}/star/%s/%s"
URL_MOVIE = f"{URL_BASE}/%s"
URL_MAGNETS = f"{URL_BASE}/ajax/uncledatoolsbyajax.php?gid=%s&lang=zh&img=/pics/cover/%s&uc=0&floor=480"

FILETYPE_IMAGE = "image"
FILETYPE_MOVIE = "movie"
FILETYPE_SUBTT = "subtitle"
FILETYPE_TORRENT = 'torrent'
FILETYPE_OTHER = 'other'

MAP_FILE_TYPE = {
    "png": FILETYPE_IMAGE, "jpg": FILETYPE_IMAGE, "jpeg": FILETYPE_IMAGE,
    "mp4": FILETYPE_MOVIE, "mkv": FILETYPE_MOVIE,
    "srt": FILETYPE_SUBTT, "ass": FILETYPE_SUBTT,
    "torrent": FILETYPE_TORRENT
}

MOVIE_RESOLUTION = {480: 'SD', 720: 'HD', 1080: 'FHD'}


def url_actors(page=1) -> str:
    return URL_ACTORS % page


def url_actor(sid: str, page=1) -> str:
    """ Return the URL of the special actress.
        :param sid:  the sid of the actress
        :param page: the page of the actress
    """
    if page < 0:
        raise
    if page == 1:
        return URL_ACTOR % sid
    else:
        return URL_ACTOR_PAGE % (sid, page)


def url_avatar(sid: str) -> str:
    return f"{URL_BASE}/pics/actress/{sid}_a.jpg"


def url_movie(code: str) -> str:
    """ Return the URL of the special movie.
        :param code:  the code of the movie
    """
    return URL_MOVIE % code


def url_magnets(movie: Movie):
    return URL_MAGNETS % (movie.gid, movie.cover)


def date_to_str(date):
    if date:
        return str(date.date())
    else:
        return '-'


def get_file_type(filename: str) -> str:
    """ Return the type of the file
        :param filename:
    """
    ext = filename.split(".")[-1]
    return MAP_FILE_TYPE.get(ext.strip(), FILETYPE_OTHER)


def save_data(data: dict, filename: str):
    try:
        with open(filename, 'w', encoding='UTF-8') as fs:
            json.dump(data, fs)
    except IOError as ioe:
        ioe.strerror = f"Unable to save data to json file ({ioe.strerror})"
        raise


def load_data(filename: str) -> dict:
    results = {}
    try:
        with open(filename, 'r', encoding='UTF-8') as fs:
            results = json.load(fs)
    except IOError as ioe:
        ioe.strerror = f"Unable to load json file ({ioe.strerror})"
        raise
    return results


def data_filter(data: dict, fields: tuple) -> dict:
    return dict(filter(lambda x: x[0] in fields, data.items()))


def get_code(filename: str) -> str | None:
    """ 从文件名中获取 Movie 的 code
       :param filename:
       :return: return the (prefix, number), 如果没有检测到，返回 (None, None)
    """
    rn = filename[::-1]
    match = re.search(r'^([0-9]{3,7})-?([a-zA-Z]{2,4})', rn)
    if match is None:
        match = re.search(r'[^0-9]+([0-9]{3,7})-?([a-zA-Z]{2,4})', rn)
    if match:
        pre = match.group(2)[::-1]
        num = match.group(1)[::-1]
        if len(num) <= 6 and len(pre) <= 4:
            if len(num) > 3:
                num = '%03d' % int(num)
        return f"{match.group(2)[::-1].upper()}-{num}"
    return None


def code(prefix: str, number: str) -> str:
    """ Generate the movie's code
       :param prefix:
       :param number:
    """
    return f"{prefix.upper()}-{number}"


def decode(movie_code: str) -> tuple[str, str]:
    pre = movie_code.split('-')[0]
    num = movie_code.split('-')[1]
    return pre, num


def is_image(filename: str) -> bool:
    return get_file_type(filename) == FILETYPE_IMAGE


def is_movie(filename: str) -> bool:
    return get_file_type(filename) == FILETYPE_MOVIE


def is_torrent(filename: str) -> bool:
    return get_file_type(filename) == FILETYPE_TORRENT


def is_subtitle(filename: str) -> bool:
    return get_file_type(filename) == FILETYPE_SUBTT


def scan_path(path: str) -> dict:
    results = {}
    for root, folders, files in os.walk(path):
        for f in files:
            code = get_code(f)
            ft = get_file_type(f)
            if code is None or ft == FILETYPE_OTHER:
                continue

            results[code] = results.get(code, {})
            results[code][ft] = results[code].get(ft, [])
            results[code][ft].append(f)
    return results


def get_basename(path: str) -> str:
    return os.path.basename(path).split('/')[-1]
