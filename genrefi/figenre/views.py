import os

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
import spotipy
import spotipy.util as util
from spotipy import oauth2
import dotenv

dotenv.read_dotenv('/home/spencer/prod/genrefi/genrefi/.env')
USERNAME = ''
SP = ''

# Create your views here.
def login(request):
    return HttpResponse(render(request,'login.html'))
    

def home(request):
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





        

    