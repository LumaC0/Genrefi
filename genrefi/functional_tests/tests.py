import time
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 3

class GenrelUserTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_login_using_OAuth_spotify_client(self):
        # Our user Chi Chi hears about a cool webapp that will give her 
        # genre information regarding her user Library
        # In short, she will access the site
        self.browser.get(self.live_server_url)
        self.assertIn('Genrefi', self.browser.title)
        # the option to login will be visible to her
        self.browser.find_element_by_id('Spotify').click()
        # she'll log into her spotify account using OAuth
        # and the spotify client
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Successfully Logged In', page_text)
