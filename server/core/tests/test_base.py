from core.utils import base


def test_dfilter():
    data = {1: 1, 2: 2, 3: 3}
    fields = [1, 2]
    assert base.data_filter(data, fields) == {1: 1, 2: 2}


def test_get_code():
    assert base.get_code("abc-001") == ('ABC', '001')
    assert base.get_code("abc-001c") == ('ABC', '001')
    assert base.get_code("test-abc-001c") == ('ABC', '001')
    assert base.get_code("example.com@TEST007C.mp4") == ('TEST', '007')
    assert base.get_code("example.com@TEXT-123-nyap2p.com") == ('TEXT', '123')
    assert base.get_code("example.com@TEXT-123_2000k.mp4") == ('TEXT', '123')
    assert base.get_code("test-abc-001ds") == ('ABC', '001')
    assert base.get_code("test-abc00001ds") == ('ABC', '001')


def test_code():
    assert base.code('abc', '001') == "ABC-001"


def test_get_file_type():
    assert base.get_file_type('test.jpg') == base.FILETYPE_IMAGE
    assert base.get_file_type('test.mkv') == base.FILETYPE_MOVIE


def test_scan_path():
    # rs = ext.scan_path('C:\\Users\\HUAWEI\\Documents')
    # print(rs)
    pass
    # assert len(rs)==2


# def test_movie_info():
#     info = base.movie_info('tests/files/41576.mp4')
#     assert info['codec_name'] == 'h264'


def test_get_magnet_hash():
    assert base.get_magnet_hash(
        "magnet:?xt=urn:btih:03eba7a9937dc7d8564a3962e74007e95f6e9b74") == "03eba7a9937dc7d8564a3962e74007e95f6e9b74"
