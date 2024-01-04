from __future__ import annotations
from logging import Logger

import requests
from requests import Response, Timeout, ConnectionError
from selenium import webdriver

headers = {"Referer": "https://javdb521.com/",
           "authority": "javdb521.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}


def http_get(url: str) -> Response | None:
    headers = {"Referer": "https://javdb521.com/",
               "authority": "javdb521.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
               }

    cookies = "list_mode=h; theme=auto; _ym_uid=1703420424102530793; _ym_d=1703420424; _ym_isad=1; over18=1; _rucaptcha_session_id=64fa5caada73b7f3bf641441577886cb; locale=en; cf_clearance=PuTnyC0tyoq1rnuA9AmY4R.lG1iSh5tpK_xtYgbHxrs-1703441555-0-2-d75b8969.2fb74d7e.cc1b015e-0.2.1703441555; _jdb_session=XAMTJ%2B8riewgTIg6QhdtRh%2FEmTyiopxjJBQ%2Bl3ZFmhkd8vz%2BB1fkMVe8PzYNLzVXERM9VA0RbtvNWD%2F6VsiMKS%2BJJDDUVatYlknZp10GXGFSYwwtItxCtp5sUk%2FJbsGVtJeHcLSNsyUXID3lPusb1u%2FWQwloqjL26Ve1c15tOw1jfwiRlKTNgk%2BYZAxCVzO3N%2BuZwGKl6vk%2BFlMbqDgZ8msShcP7ZCTUVDJ7G6uAm6H9eJzGL8gyWkvAZHpAOGdPHYn4fWD2bNeWv0J7%2Fwk6ta%2BQY3h8VnofaO6Hrx1Tlfn7nZ7bBIPMkxnT--NsDc2Nd2aCitVu8F--2FQ83MBRyI0rgZ13YV3AwA%3D%3D"

    jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies.split(";"):
        key, value = cookie.split("=", 1)
        jar.set(key, value)
    print(jar)
    try:
        return requests.get(url, cookies=jar, headers=headers)
    except Timeout as t:
        print(t)
    except ConnectionError as e:
        print(e)
    finally:
        return None


def web_get(url: str):
    browser = webdriver.Chrome()
    browser.get(url)
