from django.contrib import admin
from django.urls import path, include
from . views import IndexView
app_name = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

]
