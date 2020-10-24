from django.urls import path
from django.conf import settings
from . import views

app_name = 'OsasSystem'
urlpatterns = [
    path('', views.home, name="home"),
]