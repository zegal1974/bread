# from bs4 import BeautifulSoup
# # import re
#
# from api.utils import scan
#
#
# def test_scan_actor():
#     with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         actor = scan._scan_actor(doc)
#         # print(actor)
#         assert actor['age'] == '25'
#         assert actor['height'] == '155'
#         assert actor['bust'] == '80'
#
#
# def test_scan_movies_count():
#     with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         count = scan._scan_movies_count(doc)
#         assert count == 140
#
#
# def test_scan_movies():
#     with open('api/tests/files/star.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         movies = scan._scan_movies_list(doc)
#         print(movies[0])
#         assert len(movies) == 30
#
#
# # def test_re():
# #     match = re.match(r'([0-9]+)', "中文110文字")
# #     assert match != None
# #     assert match.group(1) == '110'
#
#
# # def test_re1():
# #     match = re.search(r'([0-9]+)', "eng110text")
# #     assert match != None
# #     assert match.group(1) == '110'
#
#
# def test_scan_genres():
#     with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         genres = scan._scan_genres(doc)
#         assert len(genres) == 7
#
#
# def test_scan_movie_actors():
#     with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         actors = scan._scan_movie_actors(doc)
#         assert len(actors) == 1
#         assert actors[0]['sid'] == 'qs6'
#
#
# def test_scan_movie_gid():
#     with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         gid = scan._scan_movie_gid(doc)
#         assert gid == '55976713876'
#
#
# def test_scan_movie():
#     with open('api/tests/files/movie.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         movie = scan._scan_movie(doc)
#         print(movie)
#         assert movie['length'] == 120
#
#
# def test_scan_movie1():
#     with open('api/tests/files/movie1.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         movie = scan._scan_movie(doc)
#         print(movie)
#         assert movie['length'] == 148
#         assert movie['director']['sid'] == '2ms'
#
#
# def test_scan_magnets():
#     with open('api/tests/files/magnets.html', 'r', encoding='UTF-8') as f:
#         doc = BeautifulSoup(f.read(), 'lxml')
#         magnets = scan._scan_magnets(doc)
#         print(magnets)
#         assert len(magnets) == 18
#         assert magnets[0]['link'] == 'magnet:?xt=urn:btih:C51925A78553AE94F068A32F27EC67860A73AD5F&dn=MIAA-837_CH.HD'
#         assert magnets[0]['shared_on'] == '2023-10-22'
