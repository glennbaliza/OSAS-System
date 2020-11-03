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

    return 'profile_pic/{year}-{month}-{day}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d')) 

class osas_r_course(models.Model):
    
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=50, verbose_name='Course Code')
    course_name = models.CharField(max_length=250, verbose_name='Course Name')
    course_add_date = models.DateField(default=now)
    course_edit_date = models.DateField(default=now)
    course_status = models.CharField(max_length=10, default='Active')
        
    def __str__(self):
        return self.course_name

class osas_r_section_and_year(models.Model):

    yas_id = models.AutoField(primary_key=True)
    yas_descriptions = models.CharField(max_length=250,  verbose_name='yr and sec desc')
    yas_dateregistered = models.DateTimeField(default=now)
    status = models.CharField(max_length=50, default='Active')
    

    def __str__(self):
        return self.yas_descriptions

class osas_r_personal_info(models.Model):

    stud_id = models.AutoField(primary_key=True)
    stud_no = models.CharField(unique=True, max_length=15, verbose_name='Student Number')
    stud_course_id = models.ForeignKey('osas_r_course', on_delete=models.CASCADE)
    stud_yas_id = models.ForeignKey('osas_r_section_and_year', on_delete=models.CASCADE)
    stud_lname = models.CharField(max_length=50, verbose_name='Last Name')
    stud_fname = models.CharField(max_length=50, verbose_name='First Name')
    stud_mname = models.CharField(max_length=50, verbose_name='Middle Name')
    stud_birthdate = models.DateField(max_length=12)
    stud_gender = models.CharField(max_length=10, verbose_name='Gender')
    stud_address = models.CharField(max_length=50, verbose_name='Student Address')
    stud_email = models.EmailField(max_length=50, verbose_name='Student Email')
    stud_m_number = models.BigIntegerField(blank=True, verbose_name='Mobile Number')
    stud_hs = models.CharField(max_length=50, verbose_name='High School')
    stud_hs_add = models.CharField(max_length=50, verbose_name='High School Address')
    stud_e_name = models.CharField(max_length=50, verbose_name='Emergency Contact Person')
    stud_e_address = models.CharField(max_length=50, verbose_name='Emergency Contact Address')
    stud_e_m_number = models.BigIntegerField(blank=True, verbose_name='Mobile Number')
    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(default=now)
    
   

    def __str__(self):
        return self.stud_no, self.stud_lname, self.stud_fname

# class osas_t_id(models.Model):

#     request_id = models.AutoField(primary_key=True)
#     date_created = models.DateTimeField(default=now)
#     date_updated = models.DateTimeField(default=now)
#     lost_id_status = models.CharField(max_length=13, default='Pending')
#     lost_stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.request_id, self.lost_id_status

# class osas_t_admission(models.Model):

#     admission_id = models.IntegerField(primary_key=True)
#     request_name = models.CharField(max_length=50, verbose_name='Name of Request')
#     request_detail = models.CharField(max_length=50, verbose_name='Request Details')
#     admission_status = models.CharField(max_length=50, verbose_name='Admission Status')
#     admission_stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.request_name, self.request_detail

class osas_r_userrole(models.Model):
    # user_role = ((1,'Student'),(2,'Head'),(3,'Staff'))

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, verbose_name='Full Name')
    user_username = models.CharField(max_length=50, verbose_name='User Name')
    user_password = models.CharField(max_length=16, verbose_name='User Password')
    user_email = models.EmailField(max_length=50, verbose_name='User Email')
    user_type = models.CharField(max_length=50, verbose_name='User Type')
    date_created = models.DateTimeField(default=now)

    # s_image = models.ImageField(upload_to=image_path, default='profile_pic/image.jpg')

 #--- for image -----#
    # def image_tag(self):
    #     return mark_safe('<img src="/userrole/media/%s" width="25" height="25" />'%(self.s_image))
        
    def __str__(self):
        return self.user_email

class osas_r_stud_registration(models.Model):

    student_id = models.AutoField(primary_key=True)
    s_fname = models.CharField(max_length=20)
    s_lname = models.CharField(max_length=20)
    s_no = models.CharField(max_length=15)
    s_password = models.CharField(max_length=16)
    s_type = models.CharField(max_length=10, default='Student')
    date_created = models.DateTimeField(default=now)
    

    def __str__(self):
        return self.s_fname, self.s_no
    



