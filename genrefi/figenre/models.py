from django.db import models

class Genres(models.Model):
    genre = models.TextField(primary_key=True, max_length=128, unique=True)


class SubGenres(models.Model):
    subgenre = models.TextField(max_length=128, unique=False)
    genre = models.ForeignKey('Genres', null=False, on_delete=models.CASCADE, default=None)
