from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('send-message/', SendMessage),
    path('get-history/', GetHistory),
    path('status-chat/', SetStatus),
    path('create-group/', CreateGroup),
    path('get-users/', GetUsers),
    path('search-users/<str:word>/', SearchUsers),
    path('get-status/<str:id_user>/', GetStatus),
    path('read-msg/<int:id_msg>/', ReadMsg),
    path('get-history-about/', GetHistoryAbout),
    path('get-users-group/<str:id_group>/', GetUsersGroup),
]
