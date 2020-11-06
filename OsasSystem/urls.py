from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


app_name = 'OsasSystem'
urlpatterns = [
    path('', views.home, name="home"),
    path('<int:stud_id>/student/student_edit.html', views.student_edit, name="student_edit"),
    path('<int:user_id>/edituser.html', views.edituser, name="edituser"),
    path('<int:course_id>course/process_course_edit.html', views.process_course_edit, name="process_course_edit"),
] 