from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from authlib.integrations.django_client import OAuth

from figenre.models import Genres, SubGenres

oauth = OAuth()

class LoginPageTest(TestCase):
    def test_login_page_response(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "login.html")

class DatabaseTests(TestCase):
    def test_initial_db_data_migration(self):
        gens = Genres.objects.all()
        self.assertEqual(gens.count(), 43)
        '''
        dnb = SubGenres.objects.filter(genre='drum and bass')
        sub_dnb = SubGenres.objects.filter(subgenre='uk dnb')
        self.assertIn(sub_dnb, dnb)
        '''