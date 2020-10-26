from django.db import models
from datetime import datetime
import os, random
from django.utils import timezone
from django.utils.html import mark_safe


now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    _now = datetime.now()

    return 'profile_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d')) 

Status = ((0, 'Disable'),(1, 'Active'),)
id_status = ((1, 'Approved'),(0, 'Pending'),)

class osas_r_course(models.Model):
 
    course_id = models.IntegerField(primary_key=True)
    course_short = models.CharField(max_length=50, verbose_name='Short Course')
    course_full = models.CharField(max_length=250, verbose_name='Full Course')
    status = models.IntegerField(default=1, choices=Status)
        
    def __str__(self):
        return self.course_id

class osas_r_section_and_year(models.Model):

    yas_id = models.IntegerField(primary_key=True)
    yas_descriptions = models.CharField(max_length=250, verbose_name='yr and sec desc')
    yas_dateregistered = models.DateField(max_length=8)
    status = models.IntegerField(default=1,choices=Status)

    def __str__(self):
        return self.yas_descriptions

class osas_r_personal_info(models.Model):

    stud_id = models.IntegerField(primary_key=True)
    stud_no = models.CharField(unique=True, max_length=13, verbose_name='Student Number')
    stud_lname = models.CharField(max_length=50, verbose_name='Last Name')
    stud_fname = models.CharField(max_length=50, verbose_name='First Name')
    stud_mname = models.CharField(max_length=50, verbose_name='Middle Name')
    stud_birthdate = models.DateField(max_length=8)
    stud_gender = models.CharField(max_length=10, verbose_name='Gender')
    stud_address = models.CharField(max_length=50, verbose_name='Student Address')
    stud_email = models.EmailField(max_length=50, verbose_name='Student Email')
    stud_hs = models.CharField(max_length=50, verbose_name='High School')
    stud_hs_add = models.CharField(max_length=50, verbose_name='High School Address')
    date_created = models.DateField(default=now)
    date_updated = models.DateField(default=now)
    stud_course = models.ForeignKey('osas_r_course', on_delete=models.CASCADE)
    stud_sec_year = models.ForeignKey('osas_r_section_and_year', on_delete=models.CASCADE)

    def __str__(self):
        return self.stud_id, self.stud_lname, self.stud_fname

class osas_r_stud_contact(models.Model):

    stud_contact_id = models.IntegerField(primary_key=True)
    stud_m_number = models.BigIntegerField(blank='', verbose_name='Mobile Number')
    stud_t_number = models.BigIntegerField(blank='', verbose_name='Telephone Number')
    date_created = models.DateField(default=now)
    date_updated = models.DateField(default=now)
    stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

    def __str__(self):
        return self.m_number, self.t_number

class osas_r_emergency_contact(models.Model):

    e_contact_id = models.IntegerField(primary_key=True)
    stud_e_name = models.CharField(max_length=50, verbose_name='Emergency Contact Person')
    stud_e_address = models.CharField(max_length=50, verbose_name='Emergency Contact Address')
    e_m_number = models.BigIntegerField(blank='', verbose_name='Mobile Number')
    e_t_number = models.BigIntegerField(blank='', verbose_name='Telephone Number')
    date_created = models.DateField(default=now)
    date_updated = models.DateField(default=now)
    stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

    def __str__(self):
        return self.stud_e_name, self.e_m_number

class osas_t_id(models.Model):

    request_id = models.IntegerField(primary_key=True)
    date_created = models.DateField(default=now)
    date_updated = models.DateField(default=now)
    lost_id_status = models.IntegerField(default=0, choices=id_status)
    lost_stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

    def __str__(self):
        return self.request_id, self.lost_id_status

class osas_t_admission(models.Model):

    admission_id = models.IntegerField(primary_key=True)
    request_name = models.CharField(max_length=50, verbose_name='Name of Request')
    request_detail = models.CharField(max_length=50, verbose_name='Request Details')
    admission_status = models.CharField(max_length=50, verbose_name='Admission Status')
    admission_stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

    def __str__(self):
        return self.request_name, self.request_detail

class osas_r_userrole(models.Model):
    user_role = ((1,'Student'),(2,'Head'),(3,'Staff'))

    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50, verbose_name='Full Name')
    user_username = models.CharField(max_length=50, verbose_name='User Name')
    user_password = models.CharField(max_length=16, verbose_name='User Password')
    user_email = models.EmailField(max_length=50, verbose_name='User Email')
    user_type = models.IntegerField(max_length=50, choices=user_role, verbose_name='User Type')

    def __str__(self):
        return self.user_username

class osas_r_stud_registration(models.Model):

    student_id = models.IntegerField(primary_key=True)
    s_fname = models.CharField(max_length=20)
    s_lname = models.CharField(max_length=20)
    s_no = models.CharField(max_length=13)
    s_password = models.CharField(max_length=16)
    date_created = models.DateField(timezone.now)
    s_image = models.ImageField(upload_to=image_path, default='profile_pic/image.jpg')

    def image_tag(self):
        return mark_safe('<img src="/OsasSystem/media/%s" width="50" height="50" />'%(self.s_image))

    def __str__(self):
        return self.s_fname, self.s_no
    



