# Genrefi

Simple Django webapp that displays Spotify user Library information. Genrefi access' a user's Spotify Library and returns its genre-representation by percentage and number of songs. You can navigate to the webpage here:

### **[www.genrefi.com](https://www.genrefi.com)**


## **Setup**

the Genrefi source code is a good place to study django and the spotify API. You can navigate **[here](https://github.com/MushinMiscellanea/genrefi/blob/main/figenre/logic/genrefi_logic.py)** for the logic written to find the percentages of each genre in a user's library.

**[This](https://spotipy.readthedocs.io/en/2.16.1/)** is the Spotipy documentation. It will run through setting environment variables and navigating to the [Spotify for Developers](https://developer.spotify.com/) page to setup and app in the dashboard

## Virtual Environment

Setup a virtual env: My preference is Pipenv
```
pip install pipenv

pipenv install requirements.txt
```
## Dependancies
```
django 3.1.3
spotipy
requests
redis
django-redis-cache
```

### For Deployment
```
gunicorn
whitenoise
```

### For Testing
```
selenium
```
## Deployment
I used [Heroku](https://devcenter.heroku.com/) as a cloud-based PaaS to serve my site. It abstracts much of the headache but still is no walk in the park

## Authors
* **Spencer Finkel** - *Initial work* - [mushinMiscellanea](https://github.com/mushinMiscellanea)
