from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
import urllib.parse
import logging
import json
import os
import sys
import random
import string
from selenium import webdriver
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class YoutubeExtension(Extension):

    def __init__(self):
        super(YoutubeExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        url = "https://youtube.com/results?search_query=" + \
            str(encoded_search) + "&page=&utm_source=opensearch"

        headers = {
            "authority": "www.youtube.com",
            "cache-control": "max-age=0",
            "dnt": "1",
            "upgrade-insecure-requests": "0",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": f"VISITOR_INFO1_LIVE={get_random_string(11)}; YSC={get_random_string(2)}--{get_random_string(7)}; GPS=0 --compressed"
        }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
            'chromedriver', options=chrome_options)

        driver.header_overrides = headers

        driver.implicitly_wait(2)  # wait seconds
        driver.get(url)
        response = driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        results = self.parse_html(soup)

        if self.max_results is not None and len(results) > self.max_results:
            return results[:self.max_results]
        return results

    def parse_html(self, soup):
        video_list = soup.select('ytd-video-renderer a#video-title')
        results = []
        for video in video_list:
            video_id = video["href"].split("=")[1]

            video_info = {
                "title": video.get("title"),
                "description": video.get("aria-label").lstrip(video.get("title")),
                "link": f'https://youtube.com/{video["href"]}',
                "thumbnail": f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'
            }
            results.append(video_info)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos})

    def on_event(self, event, extension):
        searchKeyword = event.get_argument()

        if not searchKeyword:
            return

        self.search_terms = searchKeyword
        self.max_results = 15
        self.videos = self.search()
        results = self.videos

        items = []
        for result in results:
            package = result
            logger.debug(result['title'])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=package['title'],
                                             description=package['description'],
                                             on_enter=OpenUrlAction(package['link'])))

        return RenderResultListAction(items)


if __name__ == '__main__':
    YoutubeExtension().run()
