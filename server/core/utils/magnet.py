import json
import re
import ssl
import sys
import urllib.parse
from http.client import HTTPConnection

import requests
from torrentool.api import Torrent
import urllib.request
import asyncio

import os
from core.deluge_client import DelugeRPCClient

from core import config
from core.models import Magnet

TRACKERS = [
    "wss://tracker.webtorrent.dev",
    "wss://tracker.files.fm:7073/announce",
    "ws://tracker.files.fm:7072/announce",
]


def get_magnet_hash(magnet_link: str) -> str | None:
    parsed_link = urllib.parse.urlparse(magnet_link)
    params = urllib.parse.parse_qs(parsed_link.query)

    hash_value = params.get('xt')

    if hash_value:
        return hash_value[0].split(':')[-1].upper()

    return None


def get_magnet_size(size: str):
    match = re.search(r'([\d.]+)', size)
    if match:
        return int(float(match.group(0)) * 1073741824)


def get_torrent_info(torrent_file: str) -> dict:
    torrent = Torrent.from_file(torrent_file)
    info = {'hash': torrent.info_hash, 'magnet': torrent.magnet_link, 'name': torrent.name, 'files': torrent.files,
            'source': torrent.source, 'created_on': torrent.creation_date, 'size': torrent.total_size}
    return info


def download_torrent_file(magnet_link: str):
    # if magnet_link:
    #     magnet_hash = get_magnet_hash(magnet_link)
    #     url = f"https://api.magnet-vip.com/api2/download/{magnet_hash}/"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         filename = f'{config.DIR_TORRENTS}/{magnet_hash}.torrent'
    #
    #         with open(filename, 'wb') as f:
    #             f.write(response.content)
    #         # print(f"Torrent file downloaded successfully to {filename}.")
    #         return True
    #     else:
    #         print(f"Failed to download torrent file. Response status code: {response.status_code}")
    # return False
    pass

# def client_factory(**kw):
#     """Create a disconnected client for test purposes."""
#     if sys.platform.startswith('win'):
#         auth_path = os.path.join(os.getenv('APPDATA'), 'deluge', 'auth')
#     else:
#         auth_path = os.path.expanduser("~/.config/deluge/auth")
#
#     with open(auth_path, 'rb') as f:
#         filedata = f.read().decode("utf-8").split('\n')[0].split(':')
#         print(filedata)
#
#     username, password = filedata[:2]
#     ip = '127.0.0.1'
#     port = 58846
#     kwargs = {'decode_utf8': True}
#     if kw:
#         kwargs.update(kw)
#     client = DelugeRPCClient(ip, port, username, password, **kwargs)
#     return client
#
#
# def add_torrent_magnet(magnet_link: str):
#     client = client_factory()
#     print('created client')
#     client.connect()
#
#     options = {'auto_managed': False,  # 不自动管理此任务，防止自动开始下载
#                'add_paused': True}  # 添加为暂停状态
#     torrent_id = client.call('core.add_torrent_magnet', magnet_link, options)
#     print("torrent_id" + torrent_id)
#
#
# def refresh_magnets():
#     for magnet in Magnet.objects.all():
#         if magnet.torrent is None:
#             add_torrent_magnet(magnet.link)
