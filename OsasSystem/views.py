import random
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import osas_r_userrole, osas_r_stud_registration, osas_r_course, osas_r_section_and_year, osas_r_personal_info, osas_r_referral
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

#--------------------------------------LOGIN------------------------------------------------------------------------------------------
def login(request):
    return render(request, 'login.html', {})
    
def home(request):
    return render(request, 'home.html', {})

def r_employ(request):
    return render(request, 'alumni/r_employ.html')



#--------------------------------------REGISTRATION-----------------------------------------------------------------------------------
def register(request):
    return render(request, 'register.html', {} )

def newregister(request):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    r_fname = request.POST.get('r_fname')
    r_lname = request.POST.get('r_lname')
    r_studno = request.POST.get('r_studno')
    r_username = request.POST.get('r_username')
    r_pass = request.POST.get('r_pass1')
    r_pass2 = request.POST.get('r_pass2')
    if r_pass == r_pass2:
        stud_id = osas_r_personal_info.objects.filter(stud_no = r_studno)
        if stud_id:
            s = osas_r_stud_registration.objects.filter(stud_id=osas_r_personal_info.objects.get(stud_no=r_studno))
            if s:
                messages.error(request, r_studno + ' '+ 'is already registered!')
            else:
                r = osas_r_stud_registration.objects.filter(s_username=r_username)
                if r:
                    messages.error(request, r_username + ' ' + 'is already taken!')
                else:
                    n = osas_r_stud_registration(s_fname=r_fname, s_lname=r_lname, s_username=r_username, s_password=r_pass, stud_id=osas_r_personal_info.objects.get(stud_no=r_studno))
                    n.save()
                    messages.error(request, r_studno + 'Successfully registered!')
        else:
            messages.error(request, r_studno + 'Record could not found!')
    else:
        messages.error(request, 'Password do not match!' + str(r_pass) + ' ' + str(r_pass2))
    return render(request, 'register.html')     
    
#------------------------------------YEAR AND SECTION------------------------------------------------------------------------------------
def yr_sec(request):
    user_list = osas_r_section_and_year.objects.order_by('-yas_descriptions')
    context = {'user_list': user_list}
    return render(request, 'year_section/yr_sec.html', context)

def add_yr_sec(request):
    yas_description = request.POST.get('yr_sec_desc')
    st = request.POST.get('yr_sec_status')
    today = datetime.today()
    d1 = today.strftime("%d/%m/%Y")
    try:
        n = osas_r_section_and_year.objects.get(yas_descriptions = yas_description)
        return render(request, 'year_section/yr_sec.html', {
            'error_message': "Duplicated Course Information : " 
        })
    except ObjectDoesNotExist:
        if yas_description:
            add_yr_sec = osas_r_section_and_year(yas_descriptions= yas_description,status=st)
            add_yr_sec.save()
            return HttpResponseRedirect('/yr_sec',  {'success_message': yas_description + "is added successfully"} )

#---------------------------------------------COURSE--------------------------------------------------------------------------------------------
def course(request):
    course_list = osas_r_course.objects.order_by('course_name')
    context = {'course_list': course_list}
    return render(request, 'course/course.html', {'course_list':course_list})

def course_edit(request, course_id): 
    template_name = 'course/course_edit.html'
    try:
        courses = osas_r_course.objects.get(course_id=course_id)
    except osas_r_course.DoesNotExist:
            raise Http404("Course does not exist")
    return render(request, template_name, {'courses':courses})

def process_course_edit(request, course_id):
    course = get_object_or_404(osas_r_course, pk=course_id)
    try:
        c_code = request.POST.get('course_code')
        c_name = request.POST.get('course_name')
        c_status = request.POST.get('course_status')
    except (KeyError, osas_r_userrole.DoesNotExist ):
        return render(request, 'course.html', {
            'course': course,
            'error_message': "Problem updating record",
        })
    else:
        today = datetime.today()
        course_detail = osas_r_course.objects.get(pk=course_id)
        course_detail.course_code = c_code
        course_detail.course_name = c_name
        course_detail.course_edit_date = today
        if c_status:
            course_detail.course_status = c_status
        course_detail.save()
        return HttpResponseRedirect('/course_edit' , {'success_message': "Congratulations," })

def add_course(request):
    c_code = request.POST.get('course_code')
    c_name = request.POST.get('course_name')
    c_status = request.POST.get('course_status')
    try:
        n = osas_r_course.objects.get(course_code = c_code)
        return render(request, 'course/course.html', {
            'error_message': "Duplicated Course Information : " + c_code
        })
    except ObjectDoesNotExist:
        today = datetime.today()
        d1 = today.strftime("%d/%m/%Y")
        course = osas_r_course(course_code=c_code, course_name=c_name, course_add_date=today ,course_status=c_status)
        course.save()
        return HttpResponseRedirect('/course', {'success_message': c_code + "is added successfully"})

#---------------------------------------STUDENT PROFILE--------------------------------------------------------------------------------------------
def student_profile(request):
    template_name = 'student/student_profile.html'
    student_info = osas_r_personal_info.objects.order_by('stud_no') 
    context3 = {'student_info': student_info}
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec})
  
# Populating 2 dropdown fields in 1 template from the data in 2 different table https://stackoverflow.com/questions/49353000/how-to-have-dropdown-selection-populate-datatables-table-in-template-from-django

def add_student(request):
    template_name = 'student/add_student.html'
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    return render(request, template_name, {'student_course': student_course, 'student_yr_sec': student_yr_sec})

def student_process_add(request, *args):
    l_name = request.POST.get('txt_l_name')
    f_name = request.POST.get('txt_f_name')
    m_name = request.POST.get('txt_m_name')
    studno = request.POST.get('txt_studno')
    d_of_birth = request.POST.get('date_of_birth')
    gender = request.POST.get('txt_Gender')
    address = request.POST.get('txt_address')
    email = request.POST.get('txt_email')
    mobile_number = request.POST.get('txt_mobile_number')
    course = request.POST.get('txt_course')
    yr_sec = request.POST.get('txt_yr_sec')
    h_name = request.POST.get('txt_h_name')
    h_address = request.POST.get('txt_h_address')
    e_name = request.POST.get('txt_e_name')
    e_number = request.POST.get('txt_e_number')
    e_address = request.POST.get('txt_e_address')
    try:
        n = osas_r_personal_info.objects.get(stud_no = studno)
        return HttpResponseRedirect('/student_profile' , {'error_message': "Duplicated Course Information : " + studno})
    except ObjectDoesNotExist:
        today = datetime.today()
        stud = osas_r_personal_info(stud_no = studno, stud_lname = l_name, stud_fname = f_name, stud_mname = m_name, stud_birthdate = d_of_birth,stud_gender = gender, stud_address = address, stud_email = email, stud_m_number = mobile_number, stud_hs = h_name, stud_hs_add = h_address, stud_e_name = e_name,stud_e_address = e_address, stud_e_m_number = e_number, date_created = today, stud_course_id = osas_r_course.objects.get(course_name = course), stud_yas_id  = osas_r_section_and_year.objects.get(yas_descriptions = yr_sec))
        stud.save()   
        return HttpResponseRedirect('/student_profile' , {'success_message': "Congratulations," + " " + studno + "is successfully register."})
       
def edit_student(request, stud_id): 
    template_name = 'student/edit_student.html'
    stud_course = osas_r_personal_info.objects.order_by('stud_course_id')
    context2 = {'stud_course': stud_course}
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    try:
        stud = osas_r_personal_info.objects.get(stud_id=stud_id) # query the detail thru pk
    except osas_r_personal_info.DoesNotExist:
            raise Http404("Student profile does not exist")
    return render(request, template_name,{'stud':stud,'student_course': student_course, 'stud_course':stud_course , 'student_yr_sec': student_yr_sec})

def student_edit(request, stud_id):
    stud = get_object_or_404(osas_r_personal_info, pk=stud_id)
    course = request.POST.get('txt_course')
    yr_sec = request.POST.get('txt_yr_sec')
    try:
        l_name = request.POST.get('txt_l_name')
        f_name = request.POST.get('txt_f_name')
        m_name = request.POST.get('txt_m_name')
        studno = request.POST.get('txt_studno')
        d_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('txt_Gender')
        address = request.POST.get('txt_address')
        email = request.POST.get('txt_email')
        mobile_number = request.POST.get('txt_mobile_number')
        course = request.POST.get('txt_course')
        yr_sec = request.POST.get('txt_yr_sec')
        h_name = request.POST.get('txt_h_name')
        h_address = request.POST.get('txt_h_address')
        e_name = request.POST.get('txt_e_name')
        e_number = request.POST.get('txt_e_number')
        e_address = request.POST.get('txt_e_address')
    except (KeyError, osas_r_personal_info.DoesNotExist ):
        return render(request, 'student/student_profile.html', {
            'stud': stud,
            'error_message': "Problem updating record",
        })
    else: # passing the value from template to database
        today = datetime.today()
        student_profile = osas_r_personal_info.objects.get(stud_id=stud_id)
        if studno:
            student_profile.stud_no = studno
        if d_of_birth:
            student_profile.stud_birthdate = d_of_birth
        if yr_sec:
            year_sec = osas_r_section_and_year.objects.get(yas_descriptions=yr_sec)
            student_profile.stud_yas_id = year_sec
        if course:
            crs = osas_r_course.objects.get(course_name=course)
            student_profile.stud_course_id = crs
        student_profile.stud_lname = l_name
        student_profile.stud_fname = f_name
        student_profile.stud_mname = m_name
        student_profile.stud_gender = gender
        student_profile.stud_address = address
        student_profile.stud_email = email
        student_profile.stud_m_number = mobile_number
        student_profile.stud_hs = h_name
        student_profile.stud_hs_add = h_address
        student_profile.stud_e_name = e_name
        student_profile.stud_e_address = e_address
        student_profile.stud_e_m_number = e_number
        student_profile.date_updated = today
        student_profile.save()
        return HttpResponseRedirect(reverse('edit_student', args=(stud_id,)))
      
#---------------------------------------USER ROLE-----------------------------------------------------------------------------------------
def userrole(request):
    user_list = osas_r_userrole.objects.order_by('user_type')
    context = {'user_list': user_list}
    return render(request, 'userrole.html', {'user_list': user_list})
    
def edit_user(request, user_id): 
    template_name = 'edit_user.html'
    try:
        user_role = osas_r_userrole.objects.get(user_id=user_id)
    except osas_r_userrole.DoesNotExist:
            raise Http404("User profile does not exist")
    return render(request, template_name,{'user_role':user_role})

def edituser(request, user_id):
    user = get_object_or_404(osas_r_userrole, pk=user_id)
    try:
        usertype = request.POST.get('userrole')
    except (KeyError, osas_r_userrole.DoesNotExist ):
        return render(request, 'userrole.html', {
            'user': user,
            'error_message': "Problem updating record",
        })
    else:
        today = datetime.today()
        user_profile = osas_r_userrole.objects.get(pk=user_id)
        if username:
            user_profile.user_type = usertype
        user_profile.date_updated = today
        user_profile.save()
        return HttpResponseRedirect('/userrole' , {'success_message': "Congratulations," })

def adduserrole(request):
    usertype = request.POST.get('userrole')
    try:
        n = osas_r_userrole.objects.get(user_type = usertype)
        messages.error(request, usertype +  ' ' + 'is already exist.')
        return redirect('/userrole')
    except ObjectDoesNotExist:
        today = datetime.today()
        if usertype:
            user_role = osas_r_userrole(user_type=usertype, date_created=today)
            user_role.save()
            messages.success(request, usertype + ' ' +  'Successfully Added!')
            return redirect('/userrole')
        else:
            messages.error(request, usertype + ' ' + 'is already exist.')
            return render(request, 'userrole.html', {
            'error_message': "Duplicated email : " + email
            })

def deleteuser(request):
    id = request.POST.get('del_user_id')
    osas_r_userrole.objects.get(pk=id).delete()
    return HttpResponseRedirect('/userrole')

#----------------------------------ALUMNI--------------------------------------------------------------------------------------------
def r_referral(request):
    return render(request, 'alumni/r_referral.html')

def add_ref(request):
    referral_name = request.POST.get('ref_name')
    referral_email = request.POST.get('ref_email')
    referral_contact = request.POST.get('ref_contact')
    referral_share = request.POST.get('ref_share')
    status = request.POST.get('r_status')
    try:
        ref = osas_r_referral.objects.get(ref_name = referral_name)
        return render(request, 'r_referral.html')
    except ObjectDoesNotExist:
        today = datetime.today()
        if status == 'Active':
            status = True
        else:
            status = False
        referral = osas_r_referral(ref_name=referral_name, ref_email=referral_email, ref_contact=referral_contact, ref_share=referral_share, status=status, ref_date_created=today)
        referral.save()
        return render(request, 'alumni/r_referral.html')





