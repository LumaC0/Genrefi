from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from authlib.integrations.django_client import OAuth

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return HttpResponse(render(request,'login.html'))
    