from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('send-message/', SendMessage),
    path('get-history/', GetHistory),
    path('status-chat/', SetStatus),
    path('get-history-about/', GetHistoryAbout),
]
