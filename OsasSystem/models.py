from django.db import models
from datetime import datetime
import os, random
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse


now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    _now = datetime.now()

    return 'proof_pic/{year}-{month}-{day}-{basename}-{randomstring}{ext}'.format(basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d')) 

def file_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    return '{basename}{ext}'.format(basename = basefilename, ext=file_extension)

def file_path_concept(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    return '{basename}{ext}'.format(basename = basefilename, ext=file_extension)

def return_file_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    return 'accreditation/{basename}{ext}'.format(basename = basefilename, ext=file_extension)

def file_ext(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    if file_extension == '.docx':
        return '{ext}'.format(ext='.docx')
    else:
        return '{ext}'.format(ext=file_extension)
    

class osas_r_course(models.Model):
    
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=50, verbose_name='Course Code')
    course_name = models.CharField(max_length=250, verbose_name='Course Name')
    course_add_date = models.DateTimeField(max_length=50, default=now)
    course_edit_date = models.DateField(default=now)
    course_status = models.CharField(max_length=10, default='ACTIVE')
        
    def __str__(self):
        return self.course_name

class osas_r_section_and_year(models.Model):

    yas_id = models.AutoField(primary_key=True)
    yas_descriptions = models.CharField(max_length=250,  verbose_name='yr and sec desc')
    yas_dateregistered = models.DateField(default=now)
    status = models.CharField(max_length=50, default='ACTIVE')
    
    def __str__(self):
        return self.yas_descriptions

class osas_r_personal_info(models.Model):

    stud_id = models.AutoField(primary_key=True)
    stud_no = models.CharField(unique=True, max_length=15, verbose_name='Student Number')
    stud_course_id = models.ForeignKey('osas_r_course', on_delete=models.CASCADE)
    stud_yas_id = models.ForeignKey('osas_r_section_and_year', on_delete=models.CASCADE)
    stud_role = models.ForeignKey('osas_r_userrole', on_delete=models.CASCADE, null = True)
    stud_lname = models.CharField(max_length=50, verbose_name='Last Name')
    stud_fname = models.CharField(max_length=50, verbose_name='First Name')
    stud_mname = models.CharField(max_length=50, verbose_name='Middle Name')
    stud_sname = models.CharField(max_length=50,  null=True,verbose_name='Suffix Name')
    stud_birthdate = models.DateField(max_length=12, default=now)
    stud_gender = models.CharField(max_length=10, verbose_name='Gender')
    stud_address = models.CharField(max_length=50, verbose_name='Student Address')
    stud_email = models.EmailField(max_length=50, verbose_name='Student Email')
    stud_m_number = models.BigIntegerField(blank=True, verbose_name='Mobile Number')
    stud_hs = models.CharField(max_length=50, verbose_name='High School')
    stud_hs_add = models.CharField(max_length=50, verbose_name='High School Address')
    stud_sh = models.CharField(max_length=50, blank=True, verbose_name='High School')
    stud_sh_add = models.CharField(max_length=50, blank=True, verbose_name='High School Address')
    stud_e_name = models.CharField(max_length=50, verbose_name='Emergency Contact Person')
    stud_e_address = models.CharField(max_length=50, verbose_name='Emergency Contact Address')
    stud_e_m_number = models.BigIntegerField(blank=True, verbose_name='Mobile Number')
    s_password = models.CharField(max_length=16)
    date_created = models.DateTimeField(max_length=50, blank=True)
    date_updated = models.DateTimeField(default=now)
    stud_status = models.CharField(max_length=10, default='Pending')
    
    def __str__(self):
        return self.stud_no
    
    # def __str__(self):
    #     return '{} {} {}'.format(self.stud_lname, self.stud_fname,self.stud_mname)


class osas_t_id(models.Model):
    lost_id = models.AutoField(primary_key=True)
    request_id = models.CharField(unique=True, max_length=10)
    lost_id_status = models.CharField(max_length=13, default='PENDING')
    lost_id_sanction_excuse = models.CharField(max_length=13, null=True, blank=True)
    lost_stud_id = models.ForeignKey(osas_r_personal_info, on_delete=models.CASCADE)
    date_created = models.DateField(max_length=50)
    date_updated = models.DateField(max_length=50)
    lost_id_notif_stud = models.CharField(max_length=13, null = True)
    lost_id_notif_head = models.CharField(max_length=13, null = True)
    def __str__(self):
        return str(self.lost_id)
        
# class osas_t_admission(models.Model):

#     admission_id = models.IntegerField(primary_key=True)
#     request_name = models.CharField(max_length=50, verbose_name='Name of Request')
#     request_detail = models.CharField(max_length=50, verbose_name='Request Details')
#     admission_status = models.CharField(max_length=50, verbose_name='Admission Status')
#     admission_stud_id = models.ForeignKey('osas_r_personal_info', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.request_name, self.request_detail

class osas_r_userrole(models.Model):

    user_id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50, verbose_name='User Type')
    date_created = models.DateField(max_length=50, blank=True)
    date_updated = models.DateField(default=now)

    s_image = models.ImageField(upload_to=image_path, default='proof_pic/image.jpg')

 #--- for image -----#
    # def image_tag(self):
    #     return mark_safe('<img src="/userrole/media/%s" width="25" height="25" />'%(self.s_image))
        
    def __str__(self):
        return str(self.user_id)

class osas_r_auth_user(models.Model):
    auth_id = models.AutoField(primary_key=True)
    auth_lname = models.CharField(max_length=50)
    auth_fname = models.CharField(max_length=50)
    auth_username = models.CharField(max_length=50)
    auth_password = models.CharField(max_length=16)
    auth_role = models.ForeignKey('osas_r_userrole', on_delete=models.CASCADE)
    date_created = models.DateField(max_length=50, blank=True)
    date_updated = models.DateField(default=now)
    auth_status = models.CharField(max_length=10, default='ACTIVE')
    def __str__(self):
        return str(self.auth_id)


class osas_r_disciplinary_sanction(models.Model): # ex. 1st offense, sample_desc, 16hrs, 5days
    ds_id = models.AutoField(primary_key = True)
    ds_violation_count = models.CharField(max_length = 200)
    ds_violation_desc = models.CharField(max_length = 200)
    ds_hrs = models.IntegerField()
    ds_days = models.IntegerField()
    ds_code_id = models.ForeignKey('osas_r_code_title', on_delete=models.CASCADE)
    ds_status = models.CharField(max_length = 50)
    ds_datecreated = models.DateField(default = now, null = True)
    def __str__(self):
        return str(self.ds_id)

class osas_r_designation_office(models.Model):
    designation_id = models.AutoField(primary_key = True)
    designation_office = models.CharField(max_length = 50)
    designation_datecreated = models.DateTimeField(default = now)
    def __str__(self):
        return self.designation_id

class osas_r_code_title(models.Model):
    ct_id = models.AutoField(primary_key = True)
    ct_name = models.CharField(max_length = 50)
    ct_status = models.CharField(max_length = 10, default = "Active")
    ct_datecreated = models.DateTimeField(default = now)
    def __str__(self):
        return self.ct_id

class osas_t_sanction(models.Model):
    sanction_id = models.AutoField(primary_key = True)
    sanction_control_number = models.CharField(max_length = 10)
    sanction_t_id = models.ForeignKey(osas_t_id, on_delete = models.CASCADE, null = True)
    sanction_code_id = models.ForeignKey('osas_r_disciplinary_sanction', on_delete = models.CASCADE)
    sanction_designation_id = models.ForeignKey('osas_r_designation_office', on_delete=models.CASCADE, null = True)
    sanction_auth_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)
    sanction_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE)
    sanction_t_id = models.ForeignKey('osas_t_id', on_delete = models.CASCADE, null=True)
    sanction_excuse_id = models.ForeignKey('osas_t_excuse', on_delete = models.CASCADE, null=True)
    sanction_rendered_hr = models.IntegerField()
    sanction_status = models.CharField(max_length = 50)
    sanction_startdate = models.DateField(null = True)
    sanction_enddate = models.DateField(null = True)
    sanction_datecreated = models.DateField( null=True)
    sanction_dateupdated = models.DateField(default = now)
    def __str__(self):
        return self.sanction_id

class osas_t_excuse(models.Model):
    excuse_id = models.AutoField(primary_key = True)
    excuse_reason = models.CharField(max_length = 200)
    excuse_proof = models.ImageField(upload_to=image_path, null=True, blank = True)
    excuse_status = models.CharField(max_length = 10)
    excuse_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE)
    excuse_datecreated = models.DateField(default = now)
    excuse_dateupdated = models.DateField(default = now)
    
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width = "50" height="50" />'%(self.excuse_proof))

    def __str__(self):
        return str(self.excuse_id)

#----------------------------------------------GRIEVANCES-------------------------------------------------------------
class osas_t_complaint(models.Model):
    comp_id = models.AutoField(primary_key = True)
    comp_number = models.CharField(max_length = 10, blank=True)
    comp_category = models.CharField(max_length = 50, blank=True)
    comp_nature = models.CharField(max_length = 50, blank=True)
    comp_g_assign = models.CharField(max_length = 50, blank=True)
    comp_letter = models.CharField(max_length = 2000)
    comp_pic = models.ImageField(upload_to=image_path, null=True, blank = True)
    comp_status = models.CharField(max_length = 10, default = "PENDING")
    comp_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE)
    comp_datecreated = models.DateField(default = now)
    comp_seen = models.CharField(max_length = 10, null=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width = "50" height="50" />'%(self.comp_pic))

    def __str__(self):
        return str(self.comp_id)


class osas_notif(models.Model):
    notif_id = models.AutoField(primary_key = True)
    notif_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE, null = True)
    notif_lost_id = models.ForeignKey('osas_t_id', on_delete = models.CASCADE, null = True)
    notif_sanction_id = models.ForeignKey('osas_t_sanction', on_delete = models.CASCADE, null = True)
    notif_excuse_id = models.ForeignKey('osas_t_excuse', on_delete = models.CASCADE, null = True)
    notif_complaint_id = models.ForeignKey('osas_t_complaint', on_delete = models.CASCADE, null = True)
    notif_stat = models.CharField(max_length=13, null = True)
    notif_stud = models.CharField(max_length=13, null = True)
    notif_head = models.CharField(max_length=13, null = True)
    notif_datecreated = models.DateField(default = now)

#---------------------------------------------ORGANIZATION----------------------------------------------
class classroom(models.Model):
    room_id = models.AutoField(primary_key = True)
    room_year = models.CharField(max_length = 20)
    room_sec = models.CharField(max_length = 50, null = True)
    room_email = models.EmailField(max_length = 50)
    room_pass = models.CharField(max_length = 16)
    room_course = models.CharField(max_length = 300, null = True)
    room_status = models.CharField(max_length = 10, default = 'ACTIVE')
    room_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE, null=True)
    room_submit_date = models.DateField(null = True)
    room_datecreated = models.DateField(default = now)
    room_dateupdated = models.DateField(default = now)
    room_expiration = models.DateField(null=True)
    room_fund = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.org_id)

class fund(models.Model):
    fund_id = models.AutoField(primary_key = True)
    fund_desc = models.CharField(max_length = 500, null = True)
    fund_amount = models.IntegerField()
    fund_word = models.CharField(max_length = 500)
    fund_status = models.CharField(max_length = 20, default = 'PENDING')
    fund_date_requested = models.DateField(default = now)
    fund_date_approved = models.DateField(null = True)
    fund_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    fund_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    fund_head_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)
    fund_type = models.CharField(max_length = 50, null = True)
    
    def __str__(self):
        return str(self.fund_id)

class fund_file(models.Model):
    fund_f_id = models.AutoField(primary_key = True)
    fund_fund_id = models.ForeignKey('fund', on_delete = models.CASCADE, null=True)
    fund_f_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    fund_f_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    fund_f_head_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)
    fund_f_file = models.FileField(upload_to='', null=True, blank = True)
    fund_f_file_ext = models.CharField(max_length = 20, null=True)
    fund_f_status = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.fund_f_id)

    def delete(self, *args, **kwargs):
        self.fund_f_file.delete()
        super().delete(*args, **kwargs)

class officer(models.Model):
    off_id = models.AutoField(primary_key = True)
    off_position = models.CharField(max_length = 200)
    off_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE, null=True)
    off_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    off_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    off_status = models.CharField(max_length = 20, default = 'ACTIVE')
    off_date_added = models.DateField(default = now)
    off_signature = models.FileField(upload_to='', null=True, blank = True)
    off_signature_ext = models.CharField(max_length = 20, null=True)

    def __str__(self):
        return str(self.off_id)
    
    def delete(self, *args, **kwargs):
        self.off_signature.delete()
        super().delete(*args, **kwargs)

class organization(models.Model):
    org_id = models.AutoField(primary_key = True)
    org_name = models.CharField(unique=True, max_length = 50)
    org_abbr = models.CharField(max_length = 50, null = True)
    org_email = models.EmailField(max_length = 50)
    org_pass = models.CharField(max_length = 16)
    org_status = models.CharField(max_length = 10, default = 'ACCREDITED')
    org_notes = models.CharField(max_length = 500, null=True)
    org_stud_id = models.ForeignKey('osas_r_personal_info', on_delete = models.CASCADE, null=True)
    org_submit_date = models.DateField(null = True)
    org_date_accredited = models.DateField(null = True)
    org_date_accredited_year = models.DateField(null = True)
    org_datecreated = models.DateField(default = now)
    org_dateupdated = models.DateField(default = now)
    org_expiration = models.DateField(null=True)
    org_fund = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.org_id)

class organization_chat(models.Model):
    msg_id = models.AutoField(primary_key = True)
    msg_message = models.CharField(max_length = 200)
    msg_status = models.CharField(max_length = 10, default = 'Delivered')
    msg_date = models.DateTimeField(default = now)
    msg_send_to = models.CharField(max_length = 200, null = True)
    msg_send_from = models.CharField(max_length = 200, null = True)
    msg_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    msg_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    msg_head_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)

    def __str__(self):
        return str(self.msg_id)

class org_accreditation(models.Model):
    acc_id = models.AutoField(primary_key = True)
    acc_title = models.CharField(max_length = 200, null = True)
    acc_file = models.FileField(upload_to=file_path, null=True, blank = True)
    acc_return_file = models.FileField(upload_to=return_file_path, null=True, blank = True)
    acc_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    acc_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    acc_doc_type = models.FileField(upload_to=file_ext, null=True, blank = True)
    acc_status = models.CharField(max_length = 20, default = 'SAVED')
    acc_datecreated = models.DateField(default = now)
    acc_dateupdated = models.DateField(default = now)

    def image_tag(self):
        return mark_safe('<img src="/media/accreditation/" width = "50" height="50" />'%(self.acc_file))
        
    def __str__(self):
        return self.acc_id

class concept_paper_title(models.Model):
    title_id = models.AutoField(primary_key = True)
    title_name = models.CharField(unique=True, max_length = 200)
    title_status = models.CharField(max_length = 20, null = True)
    title_datecreated = models.DateField(default = now)
    title_dateapproved = models.DateField(null = True)
    title_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    title_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    title_auth_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)

    def __str__(self):
        return str(self.title_id)

class org_concept_paper(models.Model):
    con_id = models.AutoField(primary_key = True)
    con_title_id = models.ForeignKey('concept_paper_title', on_delete = models.CASCADE, null=True)
    con_file = models.FileField(upload_to='', null=True, blank = True)
    con_org_id = models.ForeignKey('organization', on_delete = models.CASCADE, null=True)
    con_room_id = models.ForeignKey('classroom', on_delete = models.CASCADE, null=True)
    con_auth_id = models.ForeignKey('osas_r_auth_user', on_delete = models.CASCADE, null=True)
    con_file_ext = models.CharField(max_length = 20, null=True)
    con_status = models.CharField(max_length = 20, default = 'SAVED')
    con_datecreated = models.DateField(default = now)
    con_dateupdated = models.DateField(default = now)
        
    def __str__(self):
        return str(self.con_id)

    # def save(self, *args, **kwargs):
    #     self.con_file.save()
    #     super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.con_file.delete()
        super().delete(*args, **kwargs)

    
