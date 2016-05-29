from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class MusicContentTest(FunctionalTest):

    def test_main_music_page_looks_right(self):
        # The user goes to the music page
        self.browser.get(self.live_server_url + "/music/")

        # 'Learning Piano' is in the header, and the title
        self.assertIn("Learning Piano", self.browser.title)
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Learning Piano", header.text)

        # There are two videos on the page - the intro and the most recent one
        youtube_urls = [frame.get_attribute("src").split("/")[-1] for
         frame in self.browser.find_elements_by_tag_name("iframe")]
        self.assertIn("zgfARa9usiw", youtube_urls)
        self.browser.get(
         "https://www.youtube.com/channel/UCILeIbhtlv4lmgAaZbPKr8A"
        )
        latest_url = self.browser.find_element_by_class_name(
         "yt-lockup-title").find_element_by_tag_name(
          "a").get_attribute("href").split("=")[-1]
        self.assertIn(latest_url, youtube_urls)
