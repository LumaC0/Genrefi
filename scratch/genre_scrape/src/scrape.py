import os 
import re 
import pprint
import collections

import requests
from bs4 import BeautifulSoup as bs 

GENRES = collections.defaultdict(list)

class GenreScrape:

    def __init__(self):
        self.urls = [
                     'http://everynoise.com/engenremap.html',
                     'https://www.musicgenreslist.com/' ]
        self.html = None

    def __call__(self):
        self.sort_genres_by_parent()
    
    def get_html(self):
        return requests.get(self.urls[1])

    
    def parse_html(self):
        self.html = bs(self.get_html().content, 'html.parser')
        #return self.html.find_all('div', class_='genre scanme')
        return self.html.find_all('li')


    def sort_genres_by_parent(self):
        regex_key = re.compile(r'title')
        for i in self.parse_html():
            if regex_key.search(str(i)):
                genres = [a for a in i.text.split('\n') if a not in ['', '/']]
                for i in genres[1:]:
                    ind = i.find('(')
                    if ind > 0:
                        i = i[:ind]
                    GENRES[genres[0].lower()].append(i.strip().lower())   
        
            
            




if __name__=='__main__':
    scraper = GenreScrape()
    scraper()
    pp = pprint.PrettyPrinter(indent=6)
    
    pp.pprint(GENRES)

'''
    with open('genre_info.txt', 'w') as genres:
        for i in data:
            genres.write(f"{i.text.replace('» ', ' ')}\n")
'''

