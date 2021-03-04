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
        return self.user_type

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
        return self.auth_id


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

#---------------------------------------------ALUMNI-------------------------------------------------

# class osas_r_referral(models.Model):

#     ref_id = models.AutoField(primary_key=True)
#     ref_name = models.CharField(max_length=250, null=True)
#     ref_email = models.EmailField(max_length=50, blank=True)
#     ref_contact = models.BigIntegerField(max_length=11, null=True)
#     ref_share = models.CharField(max_length=250, null=True)
#     ref_date_created = models.DateTimeField(max_length=50)
#     ref_date_updated = models.DateTimeField(default=now)
#     status = models.BooleanField(default=1)

# class osas_r_educ(models.Model):
#     educ_id = models.AutoField(primary_key=True)
#     educ_bach_degree = models.CharField(max_length=500, null=False)
#     educ_graduation_date = models.DateField(max_length=12, default=now)
#     educ_attainment = models.CharField(max_length=250, null=True)
#     educ_prof_exam = models.CharField(max_length=250, null=True)
#     educ_status = models.BooleanField(default=1)
#     educ_createddate = models.DateTimeField(max_length=50)
#     educ_updatedteddate = models.DateTimeField(default=now)

# class osas_r_competencies(models.Model):
#     comp_id = models.AutoField(primary_key=True)
#     comp_theoretical = models.CharField(max_length=150, null=True)
#     comp_technical = models.CharField(max_length=150, null=True)
#     comp_english_conv = models.CharField(max_length=150, null=True)
#     comp_foreign_lang = models.CharField(max_length=150, null=True)
#     comp_ability_present_ideas = models.CharField(max_length=150, null=True)
#     comp_correspondence = models.CharField(max_length=150, null=True)
#     comp_research = models.CharField(max_length=150, null=True)
#     comp_interpersonal = models.CharField(max_length=150, null=True)
#     comp_entrep = models.CharField(max_length=150, null=True)
#     comp_basic_comp_skill = models.CharField(max_length=150, null=True)
#     comp_adv_info_tech = models.CharField(max_length=150, null=True)
#     comp_stats_soft = models.CharField(max_length=150, null=True)
#     comp_management = models.CharField(max_length=150, null=True)
#     comp_problem_solving = models.CharField(max_length=150, null=True)
#     comp_critical_thinking = models.CharField(max_length=150, null=True)
#     comp_results_orient = models.CharField(max_length=150, null=True)
#     comp_flexibility = models.CharField(max_length=150, null=True)
#     comp_acc_precision = models.CharField(max_length=150, null=True)
#     comp_ability_work = models.CharField(max_length=150, null=True)
#     comp_respect = models.CharField(max_length=150, null=True)
#     comp_independence = models.CharField(max_length=150, null=True)
#     comp_initiative = models.CharField(max_length=150, null=True)
#     comp_professionalism = models.CharField(max_length=150, null=True)
#     comp_self_confi = models.CharField(max_length=150, null=True)
#     comp_commitment = models.CharField(max_length=150, null=True)
#     comp_honesty = models.CharField(max_length=150, null=True)
#     comp_diligence = models.CharField(max_length=150, null=True)
#     comp_status = models.BooleanField(default=1)
#     comp_createddate = models.DateTimeField(max_length=50)
#     comp_updateddate = models.DateTimeField(default=now)

# class osas_r_relevant(models.Model):
#     rel_id = models.AutoField(primary_key=True)
#     rel_theoretical = models.CharField(max_length=150, null=True)
#     rel_technical = models.CharField(max_length=150, null=True)
#     rel_english_conv = models.CharField(max_length=150, null=True)
#     rel_foreign_lang = models.CharField(max_length=150, null=True)
#     rel_ability_present_ideas = models.CharField(max_length=150, null=True)
#     rel_correspondence = models.CharField(max_length=150, null=True)
#     rel_research = models.CharField(max_length=150, null=True)
#     rel_interpersonal = models.CharField(max_length=150, null=True)
#     rel_entrep = models.CharField(max_length=150, null=True)
#     rel_basic_comp_skill = models.CharField(max_length=150, null=True)
#     rel_adv_info_tech = models.CharField(max_length=150, null=True)
#     rel_stats_soft = models.CharField(max_length=150, null=True)
#     rel_management = models.CharField(max_length=150, null=True)
#     rel_problem_solving = models.CharField(max_length=150, null=True)
#     rel_critical_thinking = models.CharField(max_length=150, null=True)
#     rel_results_orient = models.CharField(max_length=150, null=True)
#     rel_flexibility = models.CharField(max_length=150, null=True)
#     rel_acc_precision = models.CharField(max_length=150, null=True)
#     rel_ability_work = models.CharField(max_length=150, null=True)
#     rel_respect = models.CharField(max_length=150, null=True)
#     rel_independence = models.CharField(max_length=150, null=True)
#     rel_initiative = models.CharField(max_length=150, null=True)
#     rel_professionalism = models.CharField(max_length=150, null=True)
#     rel_self_confi = models.CharField(max_length=150, null=True)
#     rel_commitment = models.CharField(max_length=150, null=True)
#     rel_honesty = models.CharField(max_length=150, null=True)
#     rel_diligence = models.CharField(max_length=150, null=True)
#     rel_status = models.BooleanField(default=1)
#     rel_createddate = models.DateTimeField(max_length=50)
#     rel_updatedddate = models.DateTimeField(default=now)


# class osas_r_employ(models.Model):
#     employ_id = models.AutoField(primary_key=True)
#     employ_first_job = models.CharField(max_length=250, null=False)
#     employ_howfind_1stjob = models.CharField(max_length=250, null=False)
#     employ_date1st_employ = models.DateField(max_length=12, default=now)
#     employ_date_current = models.DateField(max_length=12, default=now)
#     employ_type_work = models.CharField(max_length=100, null=True)
#     employ_work_pos = models.CharField(max_length=100, null=True)
#     employ_work_related = models.CharField(max_length=50, null=True)
#     employ_long = models.CharField(max_length=200, null=True)
#     employ_present_stat = models.CharField(max_length=250, null=True)
#     employ_job_level = models.CharField(max_length=250, null=True)
#     employ_reasons_unemployed = models.CharField(max_length=250, null=True)
#     employ_self_employed = models.CharField(max_length=200, null=True)
#     employ_area = models.CharField(max_length=250, null=True)
#     employ_address = models.CharField(max_length=250, null=True)
#     employ_nature_company = models.CharField(max_length=250, null=True)
#     employ_nature_industry = models.CharField(max_length=250, null=True)
#     employ_status = models.BooleanField(default=1)
#     employ_createddate = models.DateTimeField(max_length=50)
#     employ_updatedddate = models.DateTimeField(default=now)

# class osas_r_rate(models.Model):
#     rate_id = models.AutoField(primary_key=True)
#     rate_degree_prepared = models.CharField(max_length=200, null=True)
#     rate_practicum = models.CharField(max_length=200, null=True)
#     rate_good_career = models.CharField(max_length=200, null=True)
#     rate_degree_comp = models.CharField(max_length=250, null=True)
#     rate_my_educ = models.CharField(max_length=250, null=True)
#     rate_preferred_course = models.CharField(max_length=200, null=True)
#     rate_preferred_univ = models.CharField(max_length=200, null=True)
#     rate_satisfied = models.CharField(max_length=200, null=True)
#     rate_status = models.BooleanField(default=1)
#     rate_createddate = models.DateTimeField(max_length=50)
#     rate_updatedddate = models.DateTimeField(default=now)

# class osas_t_profile(models.Model):
#     prof_id = models.AutoField(primary_key=True)
#     prof_name = models.CharField(max_length=100, verbose_name='Last Name')
#     prof_address = models.CharField(max_length=100, verbose_name='Address')
#     prof_tel = models.BigIntegerField(blank=True, verbose_name='Telephone Number')
#     prof_mobile = models.BigIntegerField(max_length=11, verbose_name='Mobile Number')
#     prof_email = models.EmailField(max_length=50, verbose_name='User Email')
#     prof_civil_stat = models.CharField(max_length=100, verbose_name='Telephone Number')
#     prof_sex = models.CharField(max_length=100, verbose_name='Gender')
#     prof_status = models.BooleanField(default=1)
#     prof_createddate = models.DateTimeField(max_length=50)
#     prof_updateddate = models.DateTimeField(default=now)


