from django.shortcuts import render
from django.http import HttpResponse
from share.models import Script
# Module 0
# Create your views here.
def index(request):
    if request.method == "GET":
        return HttpResponse("Hello World!")
# Module 1
def get_first_script(request):
    if request.method == "GET":
        script = Script.objects.all()[0]
        return HttpResponse(str(script.title) + " " + str(script.description))
