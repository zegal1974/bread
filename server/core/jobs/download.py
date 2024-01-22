import os.path

import requests
from django_rq import job

from core.models import Movie
from core.utils.base import url_avatar
from core.utils.local import path_avatar, path_thumbnail, path_cover


def download_avatar(sid: str):
    url = url_avatar(sid)
    path = path_avatar(sid)
    download_file.delay(url, path)


def download_thumbnail(movie: Movie):
    if movie.thumbnail:
        url = movie.thumbnail
        path = path_thumbnail(movie.code)
        download_file.delay(url, path)


def download_cover(movie: Movie):
    if movie.cover:
        url = movie.cover
        path = path_cover(movie.code)
        download_file.delay(url, path)


@job('low')
def download_file(url, path) -> bool:
    print(f"Downloading {url} to {path}")
    if os.path.exists(path):
        return True

    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Failed to download {url}. Response status code: {response.status_code}")
    return False
