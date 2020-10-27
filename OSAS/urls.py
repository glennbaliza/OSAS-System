from django.contrib import admin
from django.urls import path, include
from OsasSystem import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('users/', include('OsasSystem.urls')),
    path('home/', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('userrole/', views.userrole, name="userrole"),
    path('adduserrole', views.adduserrole, name="adduserrole")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
