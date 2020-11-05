from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# from .forms import osas_r_personal_infoForm
from .models import osas_r_userrole, osas_r_stud_registration, osas_r_course, osas_r_section_and_year, osas_r_personal_info
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# from .forms import osas_r_userroleForm, osas_r_section_and_yearForm

    

def home(request):
    return render(request, 'home.html', {})

def r_employ(request):
    return render(request, 'alumni/r_employ.html')

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {} )

def yr_sec(request):
    user_list = osas_r_section_and_year.objects.order_by('-yas_descriptions')
    context = {'user_list': user_list}
    return render(request, 'year_section/yr_sec.html', context)

#need edit without form
def add_yr_sec(request):

    yas_description = request.POST.get('yr_sec_desc')
    st = request.POST.get('yr_sec_status')

    today = datetime.today()
    d1 = today.strftime("%d/%m/%Y")
    # yr_sec_desc = osas_r_section_and_year.objects.filter(yas_descriptions = yas_description )
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
   

def course(request):
    course_list = osas_r_course.objects.order_by('course_name')
    context = {'course_list': course_list}
    return render(request, 'course/course.html', context)

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


def student_profile(request):
    template_name = 'student/student_profile.html'
    student_info = osas_r_personal_info.objects.order_by('stud_no') #django will automatically reference/display the value of the child table even u select the foreingkey <3
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
    # connection.connection = None
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
    # n = osas_r_personal_info.objects.filter(stud_no = studno)
    try:
        n = osas_r_personal_info.objects.get(stud_no = studno)
        return HttpResponseRedirect('/student_profile' , {'error_message': "Duplicated Course Information : " + studno})
        # return render(request,'student/student_profile.html', {
        #     'error_message': "Duplicated student number : "
        # })
    except ObjectDoesNotExist:
        today = datetime.today()
        # d1 = today.strftime("%d/%m/%Y")
        stud = osas_r_personal_info(stud_no = studno, stud_lname = l_name, stud_fname = f_name, stud_mname = m_name, stud_birthdate = d_of_birth,stud_gender = gender, stud_address = address, stud_email = email, stud_m_number = mobile_number, stud_hs = h_name, stud_hs_add = h_address, stud_e_name = e_name,stud_e_address = e_address, stud_e_m_number = e_number, date_created = today, stud_course_id = osas_r_course.objects.get(course_name = course), stud_yas_id  = osas_r_section_and_year.objects.get(yas_descriptions = yr_sec))
        stud.save()   
        return HttpResponseRedirect('/student_profile' , {'success_message': "Congratulations," + " " + studno + "is successfully register."})
        # error handling check if the stud number exceed to the max char length or fail to meet the min char length ------------  
       
       
def edit_student(request, stud_id): 
    template_name = 'student/edit_student.html'
    stud_course = osas_r_personal_info.objects.order_by('stud_course_id')
    context2 = {'stud_course': stud_course}
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    try:
        stud = osas_r_personal_info.objects.get(stud_id=stud_id)
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
            'user': user,
            'error_message': "Problem updating record",
        })
    else:
        student_profile = osas_r_personal_info.objects.get(stud_id=stud_id)
        
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
        student_profile.save()
        return HttpResponseRedirect(reverse('edit_student', args=(stud_id,)))
      
            

def newregister(request):
    r_fname = request.POST.get('r_fname')
    r_lname = request.POST.get('r_lname')
    r_studno = request.POST.get('r_studno')
    r_pass = request.POST.get('r_pass')
    n = osas_r_stud_registration.objects.filter(s_no = r_studno).count()
    if n:
         return render(request, 'register.html', {
            'error_message': r_studno + " already registered. " 
        })
    else:
        newregister = osas_r_stud_registration(s_fname=r_fname, s_lname=r_lname, s_no=r_studno, s_password=r_pass)
        newregister.save()
        return HttpResponseRedirect('/login/', {'success_message': "Congratulations," + " " + r_studno + "is successfully register."}) 
    # try:
    #     n = osas_r_stud_registration.objects.get(s_no = r_studno)
    #     return render(request, 'register.html')
    # except ObjectDoesNotExist:
    #     newregister = osas_r_stud_registration(s_fname=r_fname, s_lname=r_lname, s_no=r_studno, s_password=r_pass)
    #     newregister.save()
    #     return HttpResponseRedirect('/login/', {
    #         'success_message': "Congratulations," + " " + r_studno + "is successfully register."}) 
            
def userrole(request):
    user_list = osas_r_userrole.objects.order_by('user_type')
    context = {'user_list': user_list}
    return render(request, 'userrole.html', context)

def adduserrole(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('userrole')
    try:
        n = osas_r_userrole.objects.get(user_email = email)
        return render(request, 'userrole.html', {
            'error_message': "Duplicated email : " + email
        })
    except ObjectDoesNotExist:
        today = datetime.today()
        if email:
            user_role = osas_r_userrole(user_name=name, user_username=username, user_password=password, user_email=email, user_type=usertype, date_created=today)
            user_role.save()
            return HttpResponseRedirect('/userrole', {'success_message': "Congratulations," + " " + name + "is successfully register."})
        return render(request, 'userrole.html', {
            'error_message': "Duplicated email : " + email
        })
#cant update the database

def edituser(request):
    id = request.POST.get('edit_user_id')
    name = request.POST.get('edit_name')
    email = request.POST.get('edit_email')
    username = request.POST.get('edit_username')
    password = request.POST.get('edit_password')
    usertype = request.POST.get('edit_userrole')
    t = osas_r_userrole.objects.filter(user_id=id)
    t.user_name = name
    t.user_username = username
    t.user_password = password 
    t.user_email = email
    t.user_type = usertype
    t.user_name.save(name) 
    t.user_username.save(username) 
    t.user_passwordrd.save(password)  
    t.user_email.save(email) 
    t.user_type.save(usertype) 
    return HttpResponseRedirect(reverse('userrole', args=(id))) 
            
def deleteuser(request):
    id = request.POST.get('del_user_id')
    osas_r_userrole.objects.get(pk=id).delete()
    return HttpResponseRedirect('/userrole')
#create a new url for update


