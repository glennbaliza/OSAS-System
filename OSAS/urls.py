from django.contrib import admin
from django.urls import path, include
from OsasSystem import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('OsasSystem.urls')),
    path('home/', views.home, name="home"),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
#---------------------------------------------LOGIN------------------------------------------------------------------------------------------------
    path('login/', views.login, name="login"),
    path('login/', views.logout, name="logout"),
    path('activate_account/', views.activate_account, name="activate_account"),
    path('account_process/', views.account_process, name="account_process"),
#-----------------------------------------REGISTRATION---------------------------------------------------------------------------------------------
 
#---------------------------------------STUDENT PROFILE--------------------------------------------------------------------------------------------
    path('student_profile/', views.student_profile, name="student_profile"),
    path('student_process_add/', views.student_process_add, name="student_process_add"),
    path('add_student/', views.add_student, name="add_student"),
    path('<int:stud_id>/edit_student/', views.edit_student, name="edit_student"),
#-------------------------------------------USER ROLE----------------------------------------------------------------------------------------------
    path('userrole/', views.userrole, name="userrole"),
    path('<int:user_id>/edit_user/', views.edit_user, name="edit_user"),
    path('adduserrole/', views.adduserrole, name="adduserrole"),
    path('deleteuser/', views.deleteuser, name="deleteuser"),

    path('auth_user/', views.auth_user, name="auth_user"),
    path('auth_user_add/', views.auth_user_add, name="auth_user_add"),
    path('<int:auth_id>/auth_process_edit/', views.auth_process_edit, name="auth_process_edit"),   
#-----------------------------------------YEAR AND SECTION-----------------------------------------------------------------------------------------
    path('yr_sec/', views.yr_sec, name="yr_sec"),
    path('add_yr_sec/', views.add_yr_sec, name="add_yr_sec"),

    path('r_employ', views.r_employ, name="r_employ"),
#--------------------------------------------COURSE------------------------------------------------------------------------------------------------
    path('course/', views.course, name="course"),  
    path('add_course/', views.add_course, name="add_course"), 
    path('<int:course_id>/course/course_edit', views.course_edit, name="course_edit"),
#--------------------------------------------ALUMNI-------------------------------------------------------------------------
    path('alumni/r_referral/', views.r_referral, name="r_referral"),
    path('add_ref/', views.add_ref, name="add_ref"),

#------------------------------------------ID-------------------------------------------------------------------------------
    path('lost_id/', views.lost_id, name="lost_id"),
    path('add_id_request/', views.add_id_request, name="add_id_request"),
    path('id_request_form/', views.id_request_form, name="id_request_form"),
    path('id_request_process/', views.id_request_process, name="id_request_process"),
    path('id_request_completed/', views.id_request_completed, name="id_request_completed"),
    path('id_request_remove/', views.id_request_remove, name="id_request_remove"),
    path('<str:request_id>/id/lost_id_view_detail', views.lost_id_view_detail, name="lost_id_view_detail"),

#--------------------------------------------STUDENT ROLE-------------------------------------------------------------------
    path('dashboard/', views.dashboard, name="dashboard"), 
    path('profile/', views.profile, name="profile"),
    path('student_lost_id/', views.student_lost_id, name="student_lost_id"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
