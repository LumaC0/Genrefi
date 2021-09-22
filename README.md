# Genrefi

``` 
Spotify has either recently updated it's terms and conditions, or I have neglected to notice, but service call limits are now granted explicility. Genrefi does not qualify for a quota extention on grounds of being a "pet project". Uninvited users can no longer sign in. There's only a 25 user limit so you can imagine the party will be dull.
```
[Spotify Terms and Conditions](https://developer.spotify.com/terms/#section-vi-access-usage-and-quotas)

A Django web application that returns statistics instead of audio signals. Specifically, the genre composition of a user's library (liked songs only). I wrote the logic because I was curious about the evolution of my music taste. To be honest, I wanted to know how much Drum and Bass I've amassed over the years. If you're curious about how much Drum and Bass, or Tame Impala, or anything else you've collected through this parilous journey, then look no further.
### **[www.genrefi.com](https://www.genrefi.com)**


## **Setup**

the Genrefi source code is a good place to study django and the spotify API. You can navigate **[here](https://github.com/MushinMiscellanea/genrefi/blob/main/figenre/logic/genrefi_logic.py)** for the logic hitting the Spotify API.

**[This](https://spotipy.readthedocs.io/en/2.16.1/)** is the Spotipy documentation. It will get you up to speed with environment variables and tasks required on the [Spotify for Developers](https://developer.spotify.com/) page to setup an app in the dashboard

## Virtual Environment

Set up a virtual env: I use Pipenv
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
I used [Heroku](https://devcenter.heroku.com/) as a cloud-based PaaS to serve my site. It abstracts much of the headache.

## Authors
* **Spencer Finkel** - [Github](https://github.com/LumaC0), [Twitter](https://twitter.com/FencerSpinkel), [Instagram](https://www.instagram.com/fencerspinkel/)
