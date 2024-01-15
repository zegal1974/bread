import json
import os
import platform
import re
import shutil
from urllib.parse import urlencode

import backoff
import requests

from cli import config


class Searcher:
    keys_from_result = ['Tracker', 'TrackerId', 'CategoryDesc', 'Title', 'Link', 'Details', 'Category', 'Size', 'Imdb']
    category_types = {'movie': 2000, 'episode': 5000}

    def __init__(self):
        self.results = []

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
    def search(self, query):
        search_url = self._get_full_search_url(query)

        resp = requests.get(search_url)

        try:
            resp_json = resp.json()
        except json.decoder.JSONDecodeError as e:
            print('Json decode error. Incident logged')
            # logger.info(f'Json decode Error. Response text: {resp.text}')
            # logger.exception(e)
            return []

        if not resp_json['Indexers']:
            info = 'No results found due to incorrectly input indexer names ({}). Check ' \
                   'your spelling/capitalization. Are they added to Jackett? Exiting...'.format(config.TRACKERS)
            print(info)
            # logger.info(info)
            return []

        # append basename to history
        # if local_release_data['basename'] not in search_history['basenames_searched']:
        #     search_history['basenames_searched'].append(local_release_data['basename'])

        self.results = self._trim_results(resp_json['Results'])
        # return self._get_matching_results(local_release_data)
        return self.results

    @staticmethod
    def _get_full_search_url(query: str):
        main_params = {
            'apikey': config.JACKETT_APIKEY,
            'Query': query
        }

        optional_params = {
            'Tracker[]': config.TRACKERS,
        }

        return config.JACKETT_SEARCH_URL + urlencode(main_params)

    def _get_matching_results(self, local_release_data):
        matching_results = []
        # print(f'Parsing { len(self.search_results) } results. ', end='')

        for result in self.results:
            max_size_difference = self.max_size_difference
            # older torrents' sizes in blutopia are are slightly off
            if result['Tracker'] == 'Blutopia':
                max_size_difference *= 2

            if abs(result['Size'] - local_release_data['size']) <= max_size_difference:
                matching_results.append(result)

        print(f'{len(matching_results)} matched of {len(self.results)} results.')
        # logger.info(f'{len(matching_results)} matched of {len(self.search_results)} results.')

        return matching_results

    # remove unnecessary values from results json
    def _trim_results(self, search_results):
        trimmed_results = []

        for result in search_results:
            new_result = {}
            for key in self.keys_from_result:
                new_result[key] = result[key]
            new_result['Title'] = self._reformat_release_name(new_result['Title'])
            trimmed_results.append(new_result)
        return trimmed_results

    @staticmethod
    def _reformat_release_name(release_name):
        release_name_re = r'^(.+?)( \[.*/.*\])?$'

        match = re.search(release_name_re, release_name, re.IGNORECASE)
        if match:
            return match.group(1)

        # logger.info(f'"{release_name}" name could not be trimmed down')
        return release_name


class Downloader:
    url_shortcut_format = '[InternetShortcut]\nURL={url}\n'
    desktop_shortcut_format = '[Desktop Entry]\n' \
                              'Encoding=UTF-8\n' \
                              'Type=Link\n' \
                              'URL={url}\n' \
                              'Icon=text-html\n'

    @staticmethod
    def download(result):
        release_name = Downloader._sanitize_name('[{Tracker}] {Title}'.format(**result))

        # if torrent file is missing, ie. Blutopia
        if result['Link'] is None:
            print(f'- Skipping release (no download link): {release_name}')
            # logger.info( f'- Skipping release (no download link): {release_name}' )
            return
        # if not ARGS.ignore_history:
        #     if HistoryManager.is_torrent_previously_grabbed(result, search_history):
        #         print( f'- Skipping download (previously grabbed): {release_name}' )
        #         logger.info( f'- Skipping download (previously grabbed): {release_name}' )
        #         return

        print(f'- Grabbing release: {release_name}')
        # logger.info(f'- Grabbing release: {release_name}')

        ext = '.torrent'
        # text data to write to file in case `result['link']` is a magnet URI
        data = ''
        if result['Link'].startswith('magnet:?xt='):
            if platform.system() == 'Windows' or platform.system() == 'Darwin':
                ext = '.url'
                data = Downloader.url_shortcut_format.format(url=result['Link'])
            else:
                ext = '.desktop'
                data = Downloader.desktop_shortcut_format.format(url=result['Link'])

        new_name = Downloader._truncate_name(release_name, ext)
        file_path = os.path.join(config.DIR_TORRENTS, new_name + ext)
        file_path = Downloader._validate_path(file_path)

        if result['Link'].startswith('magnet:?xt='):
            with open(file_path, 'w', encoding='utf8') as fd:
                fd.write(data)
        else:
            response = requests.get(result['Link'], stream=True)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

        # HistoryManager.append_to_download_history(result['Details'], result['TrackerId'], search_history)

    @staticmethod
    def _sanitize_name(release_name):
        release_name = release_name.replace('/', '-')
        release_name = re.sub(r'[^\w\-_.()\[\] ]+', '', release_name, flags=re.IGNORECASE)
        return release_name

    @staticmethod
    def _truncate_name(release_name, ext):
        """
        truncates length of file name to avoid max path length OS errors
        :param release_name (str): name of file, without file extension
        :return (str): truncated file name, without extension
        """
        # 255 length with space for nul terminator and file extension
        max_length = 254 - len(ext)
        new_name = release_name[:max_length]

        if os.name == 'nt':
            return new_name

        max_bytes = max_length
        while len(new_name.encode('utf8')) > max_bytes:
            max_length -= 1
            new_name = new_name[:max_length]

        return new_name

    @staticmethod
    def _validate_path(file_path):
        filename, ext = os.path.splitext(file_path)

        n = 1
        while os.path.isfile(file_path):
            file_path = f'{filename} ({n}){ext}'
            n += 1

        return file_path


class HistoryManager:
    search_history_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../files/SearchHistory.json')
    # Some trackers may have several proxies. This ensures that only the url path is logged
    # eg. tracker1.proxy1.org/details?id=55 != tracker1.proxy9001.org/details?id=55, but '/details?id=55' remains the same
    url_path_re = r'^https?://[^/]+(.+)'

    @staticmethod
    def get_download_history():
        try:
            with open(HistoryManager.search_history_file_path, 'r', encoding='utf8') as f:
                search_history = json.load(f)
            return search_history
        except:
            open(HistoryManager.search_history_file_path, 'w', encoding='utf8').close()
            return {
                'basenames_searched': [],
                'download_history': {}
            }

    @staticmethod
    def is_file_previously_searched(basename, search_history):
        for name in search_history['basenames_searched']:
            if basename == name:
                return True
        return False

    @staticmethod
    def is_torrent_previously_grabbed(result, search_history):
        url_path = re.search(HistoryManager.url_path_re, result['Details']).group(1)
        tracker_id = result['TrackerId']

        if search_history['download_history'].get(tracker_id) is None:
            return False

        for download_history_url_path in search_history['download_history'][tracker_id]:
            if download_history_url_path == url_path:
                return True
        return False

    @staticmethod
    def append_to_download_history(details_url, tracker_id, search_history):
        url_path = re.search(HistoryManager.url_path_re, details_url).group(1)

        if search_history['download_history'].get(tracker_id) is None:
            search_history['download_history'][tracker_id] = []

        # to prevent duplicates, in case --ignore-history flag is enabled
        if url_path not in search_history['download_history'][tracker_id]:
            search_history['download_history'][tracker_id].append(url_path)
