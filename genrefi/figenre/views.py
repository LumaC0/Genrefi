import os

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, Http404 
from django.conf import settings
from django.views import View

import spotipy
import dotenv

dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')
CACHES_FOLDER = settings.SESSION_FILE_PATH

class HomeView(View):
    scope = 'user-library-read'
    auth_manager = None 
                                            
    def get(self, request):
        if not request.session.get('access_token'):
            return self.get_client(request)
        spotify = spotipy.Spotify(auth_manager=self.auth_manager)
        #request.session['token'] = spotify._auth_headers()['Authorization']
        return redirect('/discover')


    def get_client(self, request):
        request.session.flush()
        self.auth_manager = spotipy.oauth2.SpotifyOAuth(
                                                scope=self.scope,
                                                cache_path=CACHES_FOLDER,
                                                show_dialog=True,
                                                )
        
        request.session['access_token'] = self.auth_manager.get_access_token()['access_token']
        request.session['token_type'] = self.auth_manager.get_access_token()['token_type']
        request.session['auth_token'] = request.session.get('token_type') + ' ' + request.session.get('access_token') 
        try:
            os.rmdir(CACHES_FOLDER)
        except NotADirectoryError:
            pass
        auth_url = self.auth_manager.get_authorize_url()
        return render(request, 'login.html', {'auth_url': auth_url})


class Discover(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        token = {'auth': request.session.get('auth_token', 'cocks')}
        return render(request, 'index.html', {'sorted': token})


'''
def home(request):
    #if not request.session._session_key:
    #    request.session.create()

    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(
            scope=scope,
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
    return render(request, 'index.html', {'token_' : [request.session, request.session['code']]})
'''