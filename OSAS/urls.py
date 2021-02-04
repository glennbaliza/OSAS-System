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
    path('lost_id_view/', views.lost_id_view, name="lost_id_view"),
    path('add_id_request/', views.add_id_request, name="add_id_request"),
    path('id_request_form/', views.id_request_form, name="id_request_form"),
    path('id_request_process/', views.id_request_process, name="id_request_process"),
    path('id_request_completed/', views.id_request_completed, name="id_request_completed"),
    path('id_request_remove/', views.id_request_remove, name="id_request_remove"),


#--------------------------------------------STUDENT ROLE-------------------------------------------------------------------
    path('dashboard/', views.dashboard, name="dashboard"), 
    path('profile/', views.profile, name="profile"),
    path('student_lost_id/', views.student_lost_id, name="student_lost_id"),
    path('sanctioning_role_student/', views.sanctioning_role_student, name="sanctioning_role_student"),
    path('sanctioning_excuse_add/', views.sanctioning_excuse_add, name="sanctioning_excuse_add"),

#-------------------------------------------SANCTION HEAD OSAS --------------------------------------------
    path('code_descipline/', views.code_descipline, name="code_descipline"), 
    path('ct_descipline_add/', views.ct_descipline_add, name="ct_descipline_add"), 
    path('ct_descipline_edit/', views.ct_descipline_edit, name="ct_descipline_edit"), 
    path('ct_descipline_delete/', views.ct_descipline_delete, name="ct_descipline_delete"),
    path('desciplinary_sanction/', views.desciplinary_sanction, name="desciplinary_sanction"), 
    path('desiplinary_sanction_add/', views.desiplinary_sanction_add, name="desiplinary_sanction_add"), 
    path('desciplinary_sanction_edit/', views.desciplinary_sanction_edit, name="desciplinary_sanction_edit"), 
    path('desciplinary_sanction_delete/', views.desciplinary_sanction_delete, name="desciplinary_sanction_delete"), 
    path('sanction_assign_office/', views.sanction_assign_office, name="sanction_assign_office"),
    path('sanctioning_student/', views.sanctioning_student, name="sanctioning_student"),
    path('sanctioning_student_view_excuse/', views.sanctioning_student_view_excuse, name="sanctioning_student_view_excuse"),
    path('sanctioning_student_completed/', views.sanctioning_student_completed, name="sanctioning_student_completed"),  
    path('sanction_student_list/', views.sanction_student_list, name="sanction_student_list"), 
    path('sanction_student_data/', views.sanction_student_data, name="sanction_student_data"),
    path('sanction_code_list/', views.sanction_code_list, name="sanction_code_list"), 
    path('sanction_code_data/', views.sanction_code_data, name="sanction_code_data"),
    path('sanction_student_add/', views.sanction_student_add, name="sanction_student_add"), 
    path('sanction_student_view/', views.sanction_student_view, name="sanction_student_view"),
    path('designated_office_list/', views.designated_office_list, name="designated_office_list"), 
    path('designation_office_data/', views.designation_office_data, name="designation_office_data"), 
    path('designation_office/', views.designation_office, name="designation_office"),
    path('designation_office_delete/', views.designation_office_delete, name="designation_office_delete"),
    path('designation_office_edit/', views.designation_office_edit, name="designation_office_edit"),
    path('designation_office_add/', views.designation_office_add, name="designation_office_add"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
