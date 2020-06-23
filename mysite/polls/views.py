from django.shortcuts import render
from django.http import HttpResponse

#comment added by local machine
def index(request):
    return HttpResponse("Hello , Ankit ")
