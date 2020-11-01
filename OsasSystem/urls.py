from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


app_name = 'OsasSystem'
urlpatterns = [
    path('', views.home, name="home"),
    
] 