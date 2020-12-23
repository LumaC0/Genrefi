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
    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        cache_path=CACHES_FOLDER,
        show_dialog=True,
    )
    print('here', request.session.keys())
    if not auth_manager.get_cached_token():
        authUrl = auth_manager.get_authorize_url()
        return render(request, 'login.html', {'auth_url': authUrl})
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    #request.session['token'] = spotify._auth_headers['Authorization']
    return render(request, 'index.html', {'token_' : request.session['token']})

'''
def login(request):
    return HttpResponse(render(request,'login.html'))

def auth(request):
    auth_code = auth_manager.get_authorization_code()
    if auth_code:
        auth_manager.get_access_token(auth_code)
        return redirect('home')
    else:
        auth_url = auth_manager.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth_code)
    request.session['token'] = sp._auth_headers()['Authorization']
    return redirect('home')#, {'auth': sp})
'''
    