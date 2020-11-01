from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from .models import osas_r_userrole
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import osas_r_userrole, osas_r_stud_registration, osas_r_course, osas_r_section_and_year
from django.contrib import messages
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
    yr_sec_desc = osas_r_section_and_year.objects.filter(yas_descriptions = yas_description ).count()
    if yr_sec_desc:
        # yr_sec_desc = osas_r_section_and_year.objects.filter(yas_descriptions = yas_description )
        return render(request, 'year_section/yr_sec.html', {
            # 'error_message': 'Duplicated Year and Section Descriptions '
        })
    else:
        add_yr_sec = osas_r_section_and_year(yas_descriptions= yas_description, status=st)
        add_yr_sec.save()
        return HttpResponseRedirect('/add_yr_sec',  {'success_message': yas_description + "is added successfully"} )
    # return render(request, 'year_section/add_yr_sec.html')

def student_profile(request):
    return render(request, 'student_profile.html', {})

def add_student(request):
    return render(request, 'add_student.html', {})
    
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
        user_role = osas_r_userrole(user_name=name, user_username=username, user_password=password, user_email=email, user_type=usertype)
        user_role.save()
        return HttpResponseRedirect('/userrole')

#cant update the database

def edituser(request):
    id = request.POST.get('edit_user_id')
    name = request.POST.get('edit_name')
    email = request.POST.get('edit_email')
    username = request.POST.get('edit_username')
    password = request.POST.get('edit_password')
    usertype = request.POST.get('edit_userrole')
    t = osas_r_userrole.objects.get(user_id=id)
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


