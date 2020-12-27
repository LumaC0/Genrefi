import os

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, Http404 
from django.conf import settings
from django.views import View

import spotipy
import dotenv

from figenre.logic import genrefi_logic

dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')
CACHE_FILE = settings.SESSION_FILE_PATH

class HomeView(View):
    scope = 'user-library-read'
    auth_manager = spotipy.oauth2.SpotifyOAuth(
                                                scope=scope,
                                                cache_path=CACHE_FILE,
                                                show_dialog=True,
                                                )
                                            
    def get(self, request):
        if request.GET.get('code'):
            self.auth_manager.get_access_token(request.GET.get('code'))
            self.set_session_variables(request)
            return redirect('/discover')
        auth_url = self.auth_manager.get_authorize_url()
        return render(request, 'login.html', {'auth_url': auth_url})
        
    def set_session_variables(self, request):
        access_token = self.auth_manager.get_access_token()['access_token']
        token_type = self.auth_manager.get_access_token()['token_type']
        request.session['auth_token'] = token_type + ' ' + access_token
        try:
            os.remove(CACHE_FILE)
        except NotADirectoryError as err:
            print(err)


class Discover(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        if not request.session.get('library_data'):
            request.session['library_data'] = genrefi_logic.genre_fi(request.session.get('auth_token'))
        data = request.session.get('library_data')
        return render(request, 'index.html', {'sorted': data})

        

