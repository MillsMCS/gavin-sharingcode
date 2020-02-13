from django.shortcuts import render
from django.http import HttpResponse
from share.models import Script
# Module 0
# Create your views here.
def index(request):
    if request.method == "GET":
        return HttpResponse("Hello World!")
