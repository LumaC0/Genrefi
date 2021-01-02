import os
import sys
import time
import json
import threading
import itertools
import functools
import collections
import concurrent.futures

import spotipy
import requests

from figenre.logic import sub_keys

GENRES = sub_keys.genres
AUTHORIZATION_TOKEN = None
REFESH_TOKEN = None


# all about making requests thread-save
# I do not thing requests are inharently thread-save. idk 
thread_local = threading.local()
def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

class BaseRequests:
    def __init__(self):
        self.query = 50
        self.token = AUTHORIZATION_TOKEN

    def send_data(self, data=None):
        """ 
        Function for transfering data to other parts of the program.
        This just makes it easier to see the data
        """
        return data
    
    def header(self):
        """
        request header that will never change.
        unless it changes...
        """
        return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self.token}
    
    def url(*args, **kwargs):
        """
        Dynamic approach to simple parameter manipulation of API endpoint url
        """
        ...

    def make_requests(*args, **kwargs):
        """
        Abstract method for making API requests
        Each inheriting class' soul purpose will be making API requests.
        Returns or pipes a response object to some sort of modifyer/parser
        """
        ...

    def make_concurrent_iterable(*args, **kwargs):
        """creates iterable for concurrent requests to map to make_requests"""
        ...

    def concur_requests(self, func, iterable: list, max_workers: int):
        """concurrency method that can be overriden if neccesarry"""
        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            executor.map(func, iterable)


class GetSongs(BaseRequests):
    def __init__(self):
        super().__init__()
        self.artist_info = dict()
        self.song_total = 0
        self.time_out_tries = 0
        self.song_total_iterable = self.make_concurrent_iterable()

    def __call__(self):
        super().concur_requests(self.make_requests,
                                self.song_total_iterable, 
                                len(self.song_total_iterable)
                                )
        
    def url(self, offset=0, query=0): 
        return f"https://api.spotify.com/v1/me/tracks?offset={offset}&limit={query}"

    def make_concurrent_iterable(self):
        session = get_session()
        try:
            response = session.get(self.url(query=1), headers=self.header()).json()
        except requests.exceptions.HTTPError as err:
            raise err(http_error_msg, response=self)
        if not response.get('total'):
            self.time_out_tries += 1
            if self.time_out_tries == 2:
                return 0
            AUTHORIZATION_TOKEN = REFESH_TOKEN
            self.make_concurrent_iterable()
        self.song_total = response.get('total')
        return list(range(0, self.song_total, self.query))
        #return list(range(0, 250, self.query)) # testing range so I dont cause DoS attack

    def process_song_requests(self, response):
        for i in response['items']:
            artist = i["track"]
            self.artist_info.setdefault(i["track"]["artists"][0]["id"], []).append(i["track"]["name"])
    #   ^
    #   |
    def make_requests(self, offset):
        session = get_session()
        while True:
            with session.get(self.url(offset=offset, query=self.query), headers=self.header()) as response:
                if response.status_code == 200:
                    self.process_song_requests(response.json())
                    break
                elif response.status_code == 429:
                    time.sleep(int(response.headers['Retry-After']))
                    continue
                else: response.raise_for_status
    

class GetGenres(BaseRequests):
    def __init__(self, artist_info):
        super().__init__()
        self.artist_genre_info = artist_info
        self.artists_iterable = self.make_concurrent_iterable()

    def __call__(self):
        super().concur_requests(self.make_requests, self.artists_iterable, len(self.artists_iterable))
        return self.send_data(self.artist_genre_info)

    def url(self, artist_pack: str): 
        return f"https://api.spotify.com/v1/artists?ids={artist_pack}"
    
    def make_concurrent_iterable(self):
        artists = list(self.artist_genre_info.keys())
        return [','.join(artists[i:i+50]) for i in  range(0, len(artists),50)]

    def process_artist_requests(self, response):
        for i in response['artists']:
            self.artist_genre_info[i["name"], tuple(i["genres"])] = self.artist_genre_info.pop(i["id"])
    
    def make_requests(self, artist_pack: str):
        session = get_session()
        while True:
            with session.get(self.url(artist_pack), headers=self.header()) as response:
                if response.status_code == 200:
                    self.process_artist_requests(response.json())
                    break
                elif response.status_code == 429:
                    time.sleep(int(response.headers['Retry-After']))
                    continue
                else: response.raise_for_status


class GenreAnalysis:
    def __init__(self, data, song_total):
        self.genre_song_data = data
        self.song_total = song_total #### Transfering data has proved hard #####
       
    def genre_ranking(self):
        """
        ranking genres returned from GetGenres requests
        ranking by frequency
        """
        genre_rank = collections.defaultdict(int)
        data = [i[1] for i in self.genre_song_data.keys()]
        for i in itertools.chain.from_iterable(data):
            genre_rank[i] += 1
        return genre_rank

    def sort(*args):
        """sorting songs by genre and maybe sorting other things in other ways"""
        ...

    def per_centum(*args):
        """Percentages"""
        ...


class SubgenreSort(GenreAnalysis):
    def __init__(self, data, song_total):
        super().__init__(data, song_total)
        self.sorted = {}
        self.mathed = {}

    @property
    def sort(self):
        genre_rank = self.genre_ranking()
        for i, v in self.genre_song_data.items():
            if i[1]:
                genres = [(gkey, genre_rank[gkey]) for gkey in i[1]]
                choice = sorted(genres, key=lambda x: x[1], reverse=True)[0][0]
                self.sorted.setdefault(choice, []).extend(v)
            else: self.sorted.setdefault("other",[]).extend(v)
        return self.sorted

    @property
    def per_centum(self):
        if not self.sorted:
            self.sort
        for i,v in self.sorted.items():
            self.mathed[i] = [round(len(v)/self.song_total * 100, 2), len(v)]
        data = list(sorted(self.mathed.items(), key = lambda x: x[1][0], reverse=True))
        return {i[0]:i[1] for i in data}, self.song_total

# code runner
def genre_fi(auth_token, refresh_token):
    global AUTHORIZATION_TOKEN
    AUTHORIZATION_TOKEN = auth_token
    REFESH_TOKEN = refresh_token
    sr = GetSongs()
    if not sr.song_total_iterable:
        return "timed out"
    sr()
    
    gr = GetGenres(sr.artist_info)
    gr()
    sort = SubgenreSort(gr.artist_genre_info, sr.song_total)
    return sort.per_centum

