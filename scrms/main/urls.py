from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', Main),
    path('auth/', AuthForm),
    path('authorize/', Auth),
    path('file-upload/', FileUpload),
    path('storage/<int:id>/', StorageView),
]
