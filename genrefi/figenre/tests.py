from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

from figenre.models import Genres, SubGenres

class LoginPageTest(TestCase):
    def test_login_page_response(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "login.html")
        

class DatabaseTests(TestCase):
    def test_initial_db_data_migration(self):
        gens = Genres.objects.all()
        subs = SubGenres.objects.filter(subgenre__contains='dnb').values_list('subgenre', flat=True)
        self.assertEqual(gens.count(), 43)
        self.assertTrue('uk dnb' in subs)