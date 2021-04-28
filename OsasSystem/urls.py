from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


app_name = 'OsasSystem'
urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('<int:stud_id>/student/student_edit.html', views.student_edit, name="student_edit"),
    path('<int:user_id>/edituser.html', views.edituser, name="edituser"),
    path('<int:course_id>course/process_course_edit.html', views.process_course_edit, name="process_course_edit"),
    path('<int:auth_id>/auth_user_edit.html', views.auth_user_edit, name="auth_user_edit"),
    path('/student_profile_edit.html', views.student_profile_edit, name="student_profile_edit"),
    # path('sanctioning_excuse_add/', views.sanctioning_excuse_add, name="sanctioning_excuse_add"),

] 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)