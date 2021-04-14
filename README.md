# Genrefi

A Django web application that returns statistics instead of audio signals. Specifically, the genre composition of a user's library (liked songs only). I wrote the logic because I was curious about the evolution of my music taste. To be honest, I wanted to know how much Drum and Bass I've amassed over the years. If you're curious about how much Drum and Bass, or Tame Impala, or anything else you've collected through this parilous journey called life, then look no further.
### **[www.genrefi.com](https://www.genrefi.com)**


## **Setup**

the Genrefi source code is a good place to study django and the spotify API. You can navigate **[here](https://github.com/MushinMiscellanea/genrefi/blob/main/figenre/logic/genrefi_logic.py)** for the logic hitting the Spotify API.

**[This](https://spotipy.readthedocs.io/en/2.16.1/)** is the Spotipy documentation. It will get you up to speed with environment variables and tasks required on the [Spotify for Developers](https://developer.spotify.com/) page to setup an app in the dashboard

## Virtual Environment

Setup a virtual env: I use Pipenv
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

### Deployment
```
gunicorn
whitenoise
```

### Testing
```
selenium
```
## Deployment
I used [Heroku](https://devcenter.heroku.com/) as a cloud-based PaaS to serve my site. It abstracts much of the headache but still is no walk in the park

## Authors
* **Spencer Finkel** - *Initial work* - [mushinMiscellanea](https://github.com/mushinMiscellanea)
