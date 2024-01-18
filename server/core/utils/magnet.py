import json
import ssl
import sys
import urllib.parse
from http.client import HTTPConnection

import requests
import torrentool
import urllib.request
import asyncio

import os
from core.deluge_client import DelugeRPCClient

from core import config


def get_magnet_hash(magnet_link: str) -> str | None:
    parsed_link = urllib.parse.urlparse(magnet_link)
    params = urllib.parse.parse_qs(parsed_link.query)

    hash_value = params.get('xt')

    if hash_value:
        return hash_value[0].split(':')[-1]

    return None


def get_torrent_info(torrent_file: str) -> dict:
    torrent = torrentool.torrent.Torrent.from_file(torrent_file)
    info = {}
    info['hash'] = torrent.info_hash
    info['magnet'] = torrent.magnet_link
    info['name'] = torrent.name
    info['files'] = torrent.files
    info['source'] = torrent.source
    info['created_on'] = torrent.creation_date
    return info


# http://127.0.0.1:9117/dl/0magnet/?jackett_apikey=eqmcldl4hgoosg5p1jvf3nzk79qu8l0t&path=Q2ZESjhIRWRpRmJKRTVoTXRJSWoyWDg4bE9iUXBYR1lJdjhUcHlrUDVIb0NXLVp0N2ZSWkI3UWZZemc2dHBfVjkxNF91TGFMM2V4MUNsTC1TODE1cXEwUlBwMUFNaVpfNEZGcDZOSDVBeFM5YUdCaVphZ0ZpWkVvM2FKbDhsZDVRclZHZHdJY3pPR0lrR1NWWUx4Zk1SdXlKYm8&file=SSPD-147-uncensored-HD

DHT_STATE_FILE = "/tmp/dht.state"


# async def start_dht():
#     if os.path.exists(DHT_STATE_FILE):
#         dht_server = DHTServer.load_state(DHT_STATE_FILE)
#         await dht_server.listen(settings.DHT_PORT)
#     else:
#         dht_server = DHTServer()
#         await dht_server.listen(settings.DHT_PORT)
#         await dht_server.bootstrap(settings.DHT_BOOTSTRAP_NODES)
#     return dht_server
#
#
# async def download_torrent(url: str) -> bool:
#     r = requests.get(url, allow_redirects=False)
#     redirected_url = r.headers['Location']
#     print(redirected_url)
#     if not redirected_url:
#         return False

# m2t = Magnet2Torrent(redirected_url, dht_server=settings.DHT_SERVER)
# hash_code = get_magnet_hash(redirected_url)
# torrent_fn = f"{config.DIR_TORRENTS}/{hash_code}.torrent"
# if os.path.exists(torrent_fn):
#     return True
# try:
#     filename, torrent_data = await m2t.retrieve_torrent()
#     with open(torrent_fn) as file:
#         file.write(torrent_data)
# except FailedToFetchException as e:
#     print(f"Failed: {e}")
#     return False
#
# return True
# exec_rpc(redirected_url)

#
# def exec_rpc(magnet):
#     """
#     使用 rpc，减少线程资源占用，关于这部分的详细信息科参考
#     https://aria2.github.io/manual/en/html/aria2c.html?highlight=enable%20rpc#aria2.addUri
#     """
#     conn = HTTPConnection(config.ARIA2RPC_ADDR, config.ARIA2RPC_PORT)
#     req = {
#         "jsonrpc": "2.0",
#         "id": "magnet",
#         "method": "aria2.addUri",
#         "params": [
#             [magnet],
#             {
#                 "bt-stop-timeout": str(config.STOP_TIMEOUT),
#                 "max-concurrent-downloads": str(config.MAX_CONCURRENT),
#                 "listen-port": "6881",
#                 "dir": config.SAVE_PATH,
#             },
#         ],
#     }
#     conn.request(
#         "POST", "/jsonrpc", json.dumps(req), {"Content-Type": "application/json"}
#     )
#
#     res = json.loads(conn.getresponse().read())
#     if "error" in res:
#         print("Aria2c replied with an error:", res["error"])
#

# def download_torrent1(url: str):
#     # c = Client(host="localhost", port=9091)  # , username="transmission", password="password")
#     # torrent_url = "magnet:?xt=urn:btih:e6abf70153d679f4e7d6610440303d23fdc4d25b&dn=SSPD-147-uncensored-HD&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=https%3A%2F%2Fopentracker.i2p.rocks%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce"
#     # torrent_url = "magnet:?xt=urn:btih:311C21C8215A3F493C225B66921DB671CBDB1120&dn=STARS-907"
#     # c.add_torrent(torrent_url)
#
#     # .\aria2c "magnet:?xt=urn:btih:e6abf70153d679f4e7d6610440303d23fdc4d25b&dn=SSPD-147-uncensored-HD&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=https%3A%2F%2Fopentracker.i2p.rocks%3A443%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce"
#     pass


def client_factory(**kw):
    """Create a disconnected client for test purposes."""
    if sys.platform.startswith('win'):
        auth_path = os.path.join(os.getenv('APPDATA'), 'deluge', 'auth')
    else:
        auth_path = os.path.expanduser("~/.config/deluge/auth")

    with open(auth_path, 'rb') as f:
        filedata = f.read().decode("utf-8").split('\n')[0].split(':')
        print(filedata)

    username, password = filedata[:2]
    ip = '127.0.0.1'
    port = 58846
    kwargs = {'decode_utf8': True}
    if kw:
        kwargs.update(kw)
    client = DelugeRPCClient(ip, port, username, password, **kwargs)
    return client


def add_torrent_magnet(magnet_link: str):
    client = client_factory()
    print('created client')
    client.connect()

    options = {'download_location': '',  # 设置为空或自定义路径以避免开始下载
               'auto_managed': False,  # 不自动管理此任务，防止自动开始下载
               'add_paused': True}  # 添加为暂停状态
    torrent_id = client.call('core.add_torrent_magnet', magnet_link, options)
    print("torrent_id" + torrent_id)
