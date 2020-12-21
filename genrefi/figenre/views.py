import os
import uuid

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest
from django.core.cache import caches, cache
from django.http import Http404
from django.conf import settings
import spotipy
import dotenv

dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')


def home(request):
    return render(request, 'index.html')

def login(request):
    return HttpResponse(render(request,'login.html'))

def auth(request):
    uid = str(uuid.uuid4())
    if not cache.get(uid):
        cache.set(uid, str) 

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id = os.environ['SPOTIPY_CLIENT_ID'],
        client_secret = os.environ['SPOTIPY_CLIENT_SECRET'],
        redirect_uri = os.environ['SPOTIPY_REDIRECT_URI'],
        scope='user-library-read',
        show_dialog=True,)

    if (auth_token := auth_manager.get_cached_token()):
        cache.set(uid, auth_token)
        SP = spotipy.Spotify(auth_token['access_token'])
    else: 
        auth_url = auth_manager.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    
    return render('home', 'index.html', {'token_': auth_token['access_token']})

'''
sp_oauth = oauth2.SpotifyOAuth(
        client_id = os.environ['SPOTIPY_CLIENT_ID'],
        client_secret = os.environ['SPOTIPY_CLIENT_SECRET'],
        redirect_uri = os.environ['SPOTIPY_REDIRECT_URI'],
        scope= 'user-library-read',
        cache_path='.cache-' + USERNAME,
        show_dialog=True,)
    
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    else:
        SP = spotipy.Spotify(token_info['access_token'])
    return render(request, 'index.html', {'auth': SP})
'''
    