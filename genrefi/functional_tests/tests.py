import os
import time
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import dotenv
dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')

MAX_WAIT = 3

class GenrelUserTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        if (url := os.environ.get('DJANGO_LIVE_SERVER_ADDRESS')):
            self.live_server_url = url 

    def tearDown(self):
        self.browser.quit()

    def test_user_can_login_using_OAuth_spotify_client_and_get_data(self):
        # Our user Chi Chi hears about a cool webapp that will give her 
        # genre information regarding her user Library
        # In short, she will access the site
        self.browser.get(self.live_server_url)
        #self.assertEqual('Poo', self.browser.current_url)
        login_url = self.browser.current_url
        # the option to login will be visible to her
        self.browser.find_element_by_id('login').click()
        time.sleep(1)
        # she'll log into her spotify account using OAuth
        # and the spotify client
        self.assertNotEqual(login_url, self.browser.current_url)
        #self.browser.find_element_by_id('login-username').send_keys('1243046973')
        #self.browser.find_element_by_id('login-password').send_keys('t659AA1qa!QA')
        #self.browser.find_element_by_id('login-button').click()
        # accept scope
        #self.browser.find_element_by_id('auth-accept').click()
        time.sleep(10)
        # Chi Chi clicks on 'discover' to access her library statistics
        
        self.browser.find_element_by_id("press-for-magic").click()
        # now we check how long it takes to get her info
        # and if she even gets her info
        populated_table = None
        for i in range(10):
            try:
                populated_table = self.browser.find_element_by_id('genres')
                break
            except:
                time.sleep(1)
                continue
            raise(TimeoutError)
    
        rows = populated_table.find_element_by_tag_name('tr')
        self.assertIn('drum and bass', [row.text for row in rows])
        

    
    def test_multiuser_login_and_use(self):
        ...
