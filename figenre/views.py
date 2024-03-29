import os

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, Http404 
from django.conf import settings
from django.views import View

import spotipy
#import dotenv

from figenre.logic import genrefi_logic

#dotenv.read_dotenv('../.env')
CACHE_FILE = settings.SESSION_FILE_PATH

class HomeView(View):
    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth( client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                                redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URI'),
                                                scope=scope,
                                                cache_path=CACHE_FILE,
                                                show_dialog=True,
                                                )
    def get(self, request):
        if request.GET.get('code'):
            self.auth_manager.get_access_token(request.GET.get('code'))
            self.set_session_variables(request)
            return redirect('/discover')
        request.session.flush()
        auth_url = self.auth_manager.get_authorize_url()
        return render(request, 'login.html', {'auth_url': auth_url})

    def set_session_variables(self, request):
        access_token = self.auth_manager.get_access_token()['access_token']
        token_type = self.auth_manager.get_access_token()['token_type']
        request.session['refresh_token'] = self.auth_manager.get_access_token()['refresh_token']
        request.session['auth_token'] = token_type + ' ' + access_token
        try:
            os.remove(CACHE_FILE)
        except NotADirectoryError as err:
            print(err)


class Discover(View):
    def get(self, request):
        if not request.session.get('library_data'):
            refresh_token = request.session.get('refresh_token')
            auth_token = request.session.get('auth_token')
            request.session['library_data'] = genrefi_logic.genre_fi(auth_token, refresh_token
            )
        data = request.session.get('library_data')
        if data == "timed out":
            return redirect('/')
        song_num = data[1]
        genres = data[0]
        first_genre = next(iter(genres))
        first_perc, first_num = genres[first_genre]
        proc_genres = [(genre.title(), num[0], num[1]) for genre, num in genres.items() if genre != first_genre and num[1] > 2]
        return render(request, 'index.html', 
            {'genre1': first_genre.title,
            'genre1_song_num': first_num,
            'genre1_song_percent': first_perc,
            'genres': proc_genres, 
            'song_num': song_num})

    def post(self, request):
        request.session.flush()
        return redirect('/')    
