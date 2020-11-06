from django.contrib import admin
from django.urls import path, include
from OsasSystem import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('OsasSystem.urls')),
    path('home/', views.home, name="home"),
#---------------------------------------------LOGIN------------------------------------------------------------------------------------------------
    path('login/', views.login, name="login"),
#-----------------------------------------REGISTRATION---------------------------------------------------------------------------------------------
    path('register/', views.register, name="register"),
    path('newregister/', views.newregister, name="newregister"),
#---------------------------------------STUDENT PROFILE--------------------------------------------------------------------------------------------
    path('student_profile/', views.student_profile, name="student_profile"),
    path('student_process_add/', views.student_process_add, name="student_process_add"),
    path('add_student/', views.add_student, name="add_student"),
    path('<int:stud_id>/student/edit_student', views.edit_student, name="edit_student"),
#-------------------------------------------USER ROLE----------------------------------------------------------------------------------------------
    path('userrole/', views.userrole, name="userrole"),
    path('<int:user_id>/edit_user/', views.edit_user, name="edit_user"),
    path('adduserrole/', views.adduserrole, name="adduserrole"),
    path('deleteuser/', views.deleteuser, name="deleteuser"),
#-----------------------------------------YEAR AND SECTION-----------------------------------------------------------------------------------------
    path('yr_sec/', views.yr_sec, name="yr_sec"),
    path('add_yr_sec/', views.add_yr_sec, name="add_yr_sec"),

    path('r_employ', views.r_employ, name="r_employ"),
#--------------------------------------------COURSE------------------------------------------------------------------------------------------------
    path('course/', views.course, name="course"),  
    path('add_course/', views.add_course, name="add_course"), 
    path('<int:course_id>/course/course_edit', views.course_edit, name="course_edit"),
#--------------------------------------------ALUMNI--------------------------------------------------------------------------------------------------
    path('alumni/r_referral/', views.r_referral, name="r_referral"),
    path('add_ref/', views.add_ref, name="add_ref"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
