import os


from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest
from django.core.cache import caches, cache
from django.http import Http404
from django.conf import settings
import spotipy
import dotenv

dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')
CACHES_FOLDER = settings.SESSION_FILE_PATH

def home(request):
    if not request.session._session_key:
        request.session.create()

    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=scope,
            cache_path=CACHES_FOLDER + '/' + request.session._session_key,
            show_dialog=True,
    )
    request.session['code'] = auth_manager.get_authorization_code()
    if (t := request.session.get('code')):
        auth_manager.get_access_token(t)
    print('here', request.session._session_key)
    if not auth_manager.get_cached_token():
        authUrl = auth_manager.get_authorize_url()
        return render(request, 'login.html', {'auth_url': authUrl})
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    request.session['token'] = spotify._auth_headers()['Authorization']
    return render(request, 'index.html', {'token_' : request.session['code']})
