from core.utils import magnet

from core.utils.magnet import add_torrent_magnet


def test_get_magnet_hash():
    assert magnet.get_magnet_hash(
        "magnet:?xt=urn:btih:03eba7a9937dc7d8564a3962e74007e95f6e9b74") == "03eba7a9937dc7d8564a3962e74007e95f6e9b74"


def test_get_torrent_info():
    #
    # print(torrent.announce_urls)
    # print(torrent.files)
    # print(info)
    # assert info['info_hash'] == ''
    pass


# def test_download_torrent():
#     # download_torrent(
#     #     "http://127.0.0.1:9117/dl/0magnet/?jackett_apikey=eqmcldl4hgoosg5p1jvf3nzk79qu8l0t&path=Q2ZESjhIRWRpRmJKRTVoTXRJSWoyWDg4bE9iUXBYR1lJdjhUcHlrUDVIb0NXLVp0N2ZSWkI3UWZZemc2dHBfVjkxNF91TGFMM2V4MUNsTC1TODE1cXEwUlBwMUFNaVpfNEZGcDZOSDVBeFM5YUdCaVphZ0ZpWkVvM2FKbDhsZDVRclZHZHdJY3pPR0lrR1NWWUx4Zk1SdXlKYm8&file=SSPD-147-uncensored-HD")
#     result = asyncio.run(download_torrent(
#         "http://127.0.0.1:9117/dl/0magnet/?jackett_apikey=eqmcldl4hgoosg5p1jvf3nzk79qu8l0t&path=Q2ZESjhIRWRpRmJKRTVoTXRJSWoyWDg4bE9iUXBYR1lJdjhUcHlrUDVIb0NXLVp0N2ZSWkI3UWZZemc2dHBfVjkxNF91TGFMM2V4MUNsTC1TODE1cXEwUlBwMUFNaVpfNEZGcDZOSDVBeFM5YUdCaVphZ0ZpWkVvM2FKbDhsZDVRclZHZHdJY3pPR0lrR1NWWUx4Zk1SdXlKYm8&file=SSPD-147-uncensored-HD")
#     )
#     assert result == 2
#
#
# def test_exec():
#     exec_rpc("magnet:?xt=urn:btih:311C21C8215A3F493C225B66921DB671CBDB1120&dn=STARS-907")


def test_deluge_download_torrent():
    add_torrent_magnet('magnet:?xt=urn:btih:F89414959099805BF9A4B8104B383A6D96B3E31B&dn=SSIS-875')
    assert 1 == 2
