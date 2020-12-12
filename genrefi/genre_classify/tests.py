from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

class smokeTest(TestCase):
    def test_working_tests(self):
        self.assertEqual(1+1,3)