from django.shortcuts import render
from django.http import HttpResponse
from main.views import *
from users.models import User, Message
# Create your views here.


def SendMessage(request):
    if CheckAuth(request) == False:
        return HttpResponse(status=403)



    print(CheckAuth(request))
    return HttpResponse(1)
