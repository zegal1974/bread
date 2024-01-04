from lxml import etree
from random import random
import time
from bs4 import BeautifulSoup
import selenium
from api import config
from api.scraper.parse import get_id, get_pic
# from api.utils.base import get_number
from api.utils.net import http_get
# from api.utils.scan import get_id, get_pic, get_number
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# import mechanicalsoup

MAX_PAGE_ACTORS = 500


class Scraper:

    def __init__(self):
        pass

    def create_session(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("detach", True)

        service = webdriver.ChromeService()
        self.driver = webdriver.Chrome(service=service, options=options)

    def init(self):
        self.open(config.JAVDB_URL_BASE)

    def open(self, url):
        self.driver.get(url)
        # print(self.browser.page)
        # doc = BeautifulSoup(self.browser.page, 'lxml')
        try:
            link = self.driver.find_element(
                By.CSS_SELECTOR, "a.button.is-success.is-large")
            if link:
                ActionChains(self.driver).move_to_element(
                    link).pause(random()).click().perform()
        except selenium.common.exceptions.NoSuchElementException:
            print('NoSuchElementException')

    def get_url_actors(self, page=1) -> str:
        if page == 1:
            return self.url_actors
        else:
            return self.url_actors_page % page

    def scan_all_actors(self):
        actors = []
        for i in range(1, 2):
            # print(self.get_url_actors(i))
            # req = http_get(self.get_url_actors(i))
            self.open(self.get_url_actors(i))
            # if req is None or req.status_code == 404:
            #     break
            # actors = actors + self._scan_actors_list(content)
            links = self.driver.find_elements(
                By.CSS_SELECTOR, "#actors.actors .actor-box a")
            for link in links:
                actor = {}
                actor['sid'] = link.get_attribute('href').split('/')[-1]
                actor['name'] = link.get_attribute('title')

                img = link.find_element(By.CSS_SELECTOR, 'img.avatar')
                actor['avatar'] = img.get_attribute('src')

                time.sleep(random.random())
                actors.append(actor)

        # ext.save_data(actresses, FILE_ACTRESS)
        return actors

    def _scan_actors_list(content) -> dict:
        """ 解析一个 actor 的列表 HTML 页面内容，生成 actor 详细列表.
          :param content: HTML content of an actors' list
        """
        actors = []
        doc = BeautifulSoup(content, 'lxml')
        links = doc.search("#actors .actors a")
        for link in links:
            actor = {}
            actor['sid'] = get_id(link['href'])
            actor['name'] = link['title']

            img = link.search('img.avatar')
            actor['avatar'] = get_pic(img['src'])

            actors.append(actor)
        return actors

    def find_element(content, css: str):
        return content.search(css)

    def find_elements(content, css_root: str, nodes: dict) -> dict:
        content.search(css_root)
        # root.

