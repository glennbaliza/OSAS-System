from django.contrib import admin
from django.urls import path, include
from OsasSystem import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('OsasSystem.urls')),
    path('home/', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('student_profile/', views.student_profile, name="student_profile"),
    path('add_student/', views.add_student, name="add_student"),
    path('student_process_add/', views.student_process_add, name="student_process_add"),
    path('userrole/', views.userrole, name="userrole"),
    path('adduserrole/', views.adduserrole, name="adduserrole"),
    path('newregister/', views.newregister, name="newregister"),
    path('deleteuser/', views.deleteuser, name="deleteuser"),
    path('edituser/', views.edituser, name="edituser"),
    path('yr_sec/', views.yr_sec, name="yr_sec"),
    path('add_yr_sec/', views.add_yr_sec, name="add_yr_sec"),
    path('r_employ', views.r_employ, name="r_employ"),
    path('course/', views.course, name="course"),  
    path('add_course/', views.add_course, name="add_course"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
