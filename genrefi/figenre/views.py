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

caches_folder = settings.SESSION_FILE_PATH
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def home(request, **kwargs):
    val = request.session['token']
    return render(request, 'index.html', {'token_' : val})

def login(request):
    return HttpResponse(render(request,'login.html'))

def auth(request):
    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        cache_path=caches_folder,
        show_dialog=True,
    )

    auth_code = auth_manager.get_authorization_code()
    #if not auth_code:
    #    auth_url = auth_manager.get_authorize_url()
    #    return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth_code)
    request.session['token'] = sp._auth_headers()['Authorization']
    return redirect('home')#, {'auth': sp})

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
    