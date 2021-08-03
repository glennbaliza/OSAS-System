import random
import os.path
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import osas_r_userrole, osas_r_course, osas_r_section_and_year, osas_r_personal_info, osas_r_auth_user, organization, org_accreditation, organization_chat, org_concept_paper,classroom, concept_paper_title, fund, officer, fund_file
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime, date, timedelta
from dateutil import parser 
from django.views.decorators.csrf import csrf_exempt
import re
import json
from django.db.models import Q
import time
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def organization_fund_info(request):
    org_data = organization.objects.all().order_by('org_abbr')
    org_info = list()
    for x in org_data:
        deposit_tot = 0
        request_tot = 0
        org_abbr = x.org_abbr
        org_bal = x.org_fund
        org_id = x.org_id
        try:
            f = fund.objects.filter(fund_org_id = organization.objects.get(org_id = org_id))
            for a in f:
                if a.fund_type == 'REQUEST':
                    request_tot = request_tot + a.fund_amount
                elif a.fund_type == 'DEPOSIT':
                    deposit_tot = deposit_tot + a.fund_amount
        except ObjectDoesNotExist:
            print('error')
        org_info.append([org_abbr,org_bal,deposit_tot,request_tot])
      
    print(org_info)
    return JsonResponse({'data': org_info})

def osas_changepass_verify(request):
    old_password = request.POST.get('old_pass')
    try:
        o = osas_r_auth_user.objects.get(auth_id = request.session['session_user_id'], auth_password = old_password)
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)

def osas_changepass(request):
    new_pass = request.POST.get('new_pass')
    try:
        o = osas_r_auth_user.objects.get(auth_id = request.session['session_user_id'])
        o.auth_password = new_pass
        o.save()
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)

def home(request):
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)   
    
    if acad_year:
    

        stud_bbtled =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BBTLEDHE')).count()
        stud_bsit =  osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSIT')).count()
        stud_bsbamm =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBA-MM')).count()
        stud_bsbahrm = osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBAHRM')).count()
        stud_bsent =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSENTREP')).count()
        stud_domt =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'DOMTMOM')).count()

        student_count = osas_r_personal_info.objects.all().count()

        no_events = concept_paper_title.objects.filter().filter(title_datecreated__contains = year ).count()
        no_accomplished = concept_paper_title.objects.filter(title_status = 'ACCOMPLISHED', title_datecreated__contains = year).count()
        no_accreditted = organization.objects.filter(org_status = 'ACCREDITED', org_date_accredited__contains = year).count()

        lost_id_completed= organization.objects.filter(org_status__iexact = 'ACCREDITED', org_date_accredited__contains = year).count()
        lost_id_process = organization.objects.filter(org_status__iexact = 'INACTIVE', org_submit_date__contains = year).count()
        lost_id_pending = organization.objects.filter(org_status__iexact = 'DISMISSED', org_submit_date__contains = year).count()


        sanction_pending = concept_paper_title.objects.filter(title_status__iexact = 'PENDING', title_datecreated__contains = year).count()
        sanction_active = concept_paper_title.objects.filter(title_status__iexact = 'VALIDATED', title_datecreated__contains = year).count()
        sanction_completed = concept_paper_title.objects.filter(title_status__iexact = 'APPROVED', title_dateapproved__contains = year).count()
        sanction_excused = concept_paper_title.objects.filter(title_status__iexact = 'ACCOMPLISHED', title_date_accomplished__contains = year).count()
        
        return render(request, 'home.html', {'stud_bbtled':stud_bbtled, 'stud_bsit':stud_bsit, 'stud_bsbamm':stud_bsbamm, 'stud_bsbahrm':stud_bsbahrm, 'stud_bsent':stud_bsent, 'stud_domt':stud_domt, 'lost_id_pending':lost_id_pending, 'lost_id_process':lost_id_process, 'lost_id_completed':lost_id_completed, 'sanction_pending':sanction_pending, 'sanction_active':sanction_active, 'sanction_completed':sanction_completed, 'sanction_excused':sanction_excused,'no_events':no_events, 'no_accomplished':no_accomplished, 'no_accreditted':no_accreditted})
    else:

        stud_bbtled =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BBTLEDHE')).count()
        stud_bsit =  osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSIT')).count()
        stud_bsbamm =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBA-MM')).count()
        stud_bsbahrm = osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBAHRM')).count()
        stud_bsent =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSENTREP')).count()
        stud_domt =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'DOMTMOM')).count()

        student_count = osas_r_personal_info.objects.all().count()
     

        no_events = concept_paper_title.objects.filter().count()
        no_accomplished = concept_paper_title.objects.filter(title_status = 'ACCOMPLISHED').count()
        no_accreditted = organization.objects.filter(org_status = 'ACCREDITED').count()

        lost_id_completed= organization.objects.filter(org_status__iexact = 'ACCREDITED').count()
        lost_id_process = organization.objects.filter(org_status__iexact = 'INACTIVE').count()
        lost_id_pending = organization.objects.filter(org_status__iexact = 'DISMISSED').count()


        sanction_pending = concept_paper_title.objects.filter(title_status__iexact = 'PENDING').count()
        sanction_active = concept_paper_title.objects.filter(title_status__iexact = 'VALIDATED').count()
        sanction_completed = concept_paper_title.objects.filter(title_status__iexact = 'APPROVED').count()
        sanction_excused = concept_paper_title.objects.filter(title_status__iexact = 'ACCOMPLISHED').count()
        
        return render(request, 'home.html', {'stud_bbtled':stud_bbtled, 'stud_bsit':stud_bsit, 'stud_bsbamm':stud_bsbamm, 'stud_bsbahrm':stud_bsbahrm, 'stud_bsent':stud_bsent, 'stud_domt':stud_domt, 'lost_id_pending':lost_id_pending, 'lost_id_process':lost_id_process, 'lost_id_completed':lost_id_completed, 'sanction_pending':sanction_pending, 'sanction_active':sanction_active, 'sanction_completed':sanction_completed, 'sanction_excused':sanction_excused, 'no_events':no_events, 'no_accomplished':no_accomplished, 'no_accreditted':no_accreditted})


#--------------------------------------LOGIN------------------------------------------------------------------------------------------
def welcome(request):
    return render(request, 'welcome.html')

def login(request):
    student_course = osas_r_course.objects.order_by('course_name')
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    try:
        del request.session['session_user_role']
        request.session['session_user_role'] = 'none'
        return render(request, 'login.html', {'student_course':student_course, 'student_yr_sec':student_yr_sec})
    except KeyError:
        return render(request, 'login.html', {'student_course':student_course, 'student_yr_sec':student_yr_sec})

def logout(request):
    try:
        del request.session['session_user_role']
        request.session['session_user_role'] = 'none'
        return render(request, 'login.html', {})
    except KeyError:
        return render(request, 'login.html', {})

def register_organization(request):
    course_list =  osas_r_course.objects.all().order_by("course_name")
    year_sec_list = osas_r_section_and_year.objects.all().order_by("-yas_descriptions")
    return render(request, 'organization_register.html', {'year_sec_list':year_sec_list, 'course_list':course_list})

def activate_account(request):
    s_no = request.POST.get('stud_no')
    password = request.POST.get('pass')
    try:
        stud = osas_r_personal_info.objects.get(stud_no = s_no)
        c = osas_r_personal_info.objects.filter(stud_no=s_no, s_password= password )
        if c:
            if stud.stud_status == 'Pending':
                return render(request, 'activate_account.html', {'stud': stud})  
            else:
                s = osas_r_userrole.objects.get(user_type = stud.stud_role.user_type)
                request.session['session_user_id'] = stud.stud_id
                request.session['session_user_no'] = stud.stud_no
                request.session['session_user_lname'] = stud.stud_lname
                request.session['session_user_fname'] = stud.stud_fname
                request.session['session_user_pass'] = stud.s_password
                request.session['session_user_role'] = s.user_type
                return HttpResponseRedirect('/profile') #passing the values of student to the next template
        else:
            messages.error(request, 'Either student number or password are incorrect.')
            return HttpResponseRedirect('/login')
    except ObjectDoesNotExist:
        u = osas_r_auth_user.objects.filter(auth_username=s_no).count()
        c = organization.objects.filter(org_email=s_no)
        if u:
            r = osas_r_auth_user.objects.get(auth_username = s_no)
            if r.auth_status == "ACTIVE":
                if r.auth_username == s_no and r.auth_password == password:
                    if r.auth_role_id == 2:
                        request.session['session_user_id'] = r.auth_id
                        request.session['session_user_lname'] = r.auth_lname
                        request.session['session_user_fname'] = r.auth_fname
                        request.session['session_user_username'] = r.auth_username
                        request.session['session_user_pass'] = r.auth_password
                        request.session['session_user_role'] = r.auth_role.user_type
                        return HttpResponseRedirect('/home', {'notif':notif})
                    else: 
                        request.session['session_user_id'] = r.auth_id
                        request.session['session_user_lname'] = r.auth_lname
                        request.session['session_user_fname'] = r.auth_fname
                        request.session['session_user_username'] = r.auth_username
                        request.session['session_user_pass'] = r.auth_password
                        request.session['session_user_role'] = r.auth_role.user_type
                        return HttpResponseRedirect('/home')
                else: 
                    messages.error(request, 'Incorrect password, please try again.')
                    return HttpResponseRedirect('/login')
            else: 
                messages.error(request, 'Your account is deactivated, failed to login.')
                return HttpResponseRedirect('/login')
        elif c:
            r = organization.objects.filter(org_email=s_no, org_pass= password)
            if r:
                c = organization.objects.get(org_email=s_no, org_pass= password)
                request.session['session_user_id'] = c.org_id
                request.session['session_user_no'] = c.org_email
                request.session['session_user_role'] = c.org_name
                request.session['session_org_abbr'] = c.org_abbr
                request.session['session_org_status'] = c.org_status
                value_list = organization_chat.objects.filter(msg_status = 'Delevired', msg_send_to = request.session['session_org_abbr']).count()
                return HttpResponseRedirect('/organization_home', {'value_list':value_list})
            else:
                messages.error(request, 'Incorrect password, please try again.')
                return HttpResponseRedirect('/login')
        else:
            room = classroom.objects.filter(room_email = s_no)
            if room:
                room2 = classroom.objects.filter(room_email = s_no, room_pass = password)
                if room2:
                    room3 = classroom.objects.get(room_email = s_no, room_pass = password)
                    request.session['session_user_id'] = room3.room_id
                    request.session['session_user_lname'] = room3.room_stud_id.stud_course_id.course_name + ' ' + room3.room_year
                    request.session['session_class_year'] = room3.room_year
                    request.session['session_user_username'] = room3.room_email
                    return HttpResponseRedirect('/classroom_home')
                else:
                    messages.error(request,  'Incorrect password, please try again.')
                    return HttpResponseRedirect('/login')
            else:
                messages.error(request,  'Invalid username, please try again.')
                return HttpResponseRedirect('/login')
        messages.error(request, 'Invalid username, please try again.')
        return HttpResponseRedirect('/login')

    
#------------------------------------YEAR AND SECTION------------------------------------------------------------------------------------
def yr_sec(request):
    status = request.POST.get('filter_status')

    if status:
            user_list = osas_r_section_and_year.objects.all().filter(status = status ).order_by('yas_descriptions')
            context = {'user_list': user_list}
            return render(request, 'year_section/yr_sec.html', {'user_list':user_list})
    else:   
        user_list = osas_r_section_and_year.objects.all().filter(status = "ACTIVE").order_by('yas_descriptions')
        context = {'user_list': user_list}
        return render(request, 'year_section/yr_sec.html', {'user_list':user_list})
    

def add_yr_sec(request):
    year_sec_name = request.POST.get('year_sec_name')
    try:
        n = osas_r_section_and_year.objects.get(yas_descriptions = year_sec_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        if year_sec_name:
            add_yr_sec = osas_r_section_and_year(yas_descriptions= year_sec_name)
            add_yr_sec.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)

def deactivate_yr_sec(request):
    yas_id = request.POST.get("yas_id")
    try:
        n = osas_r_section_and_year.objects.get(yas_id = yas_id)
        status_btn = n.status
        if status_btn == "ACTIVE":
            status_btn = "INACTIVE"
        else:
            status_btn = "ACTIVE"
        n.status = status_btn
        n.save()
        data = {
            'deleted':True,
            'id':n.yas_id,
            'yas_descriptions':n.yas_descriptions,
            'status':n.status,
            'yas_dateregistered':n.yas_dateregistered,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def edit_yr_sec(request):
    yas_id = request.POST.get('yas_id')
    try:
        n = osas_r_section_and_year.objects.get(yas_id = yas_id)
        data = {
            'success':True,
            'id':n.yas_id,
            'yas_descriptions':n.yas_descriptions,
            'status':n.status,
            'yas_dateregistered':n.yas_dateregistered,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def update_yr_sec(request):
    yr_id = request.POST.get('yr_id')
    year_sec_name1 = request.POST.get('year_sec_name1')
    try:
        u = osas_r_section_and_year.objects.get(yas_id = yr_id)
        original_yr = u.yas_descriptions 
        if year_sec_name1:
            try:
                u = osas_r_section_and_year.objects.get(yas_descriptions = year_sec_name1)
                if original_yr == year_sec_name1:
                    u.yas_descriptions = year_sec_name1
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                else:
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                u.yas_descriptions = year_sec_name1
                u.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
#---------------------------------------------COURSE--------------------------------------------------------------------------------------------
def course(request):
    filter_code = request.POST.get('filter_code')
    filter_name = request.POST.get('filter_name')
    status = request.POST.get('filter_status')
    course_lists = osas_r_course.objects.order_by('course_name')
    if filter_code and filter_name:
        if status:
            course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_name = filter_name, course_status = status ).order_by('course_code')
            return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists })
        else:   
            course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_name = filter_name).order_by('course_code')
            return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    elif filter_code and status:
        course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    elif filter_name and status:
        course_list = osas_r_course.objects.all().filter(course_name = filter_name, course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    elif status:
        course_list = osas_r_course.objects.all().filter(course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    elif filter_name:
        course_list = osas_r_course.objects.all().filter(course_name = filter_name ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    elif filter_code:
        course_list = osas_r_course.objects.all().filter(course_code = filter_code ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})
    else:
        course_list = osas_r_course.objects.all().filter(course_status = "ACTIVE").order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists})

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

def edit_course(request):
    course_id = request.POST.get('course_id')
    try:
        n = osas_r_course.objects.get(course_id = course_id)
        data = {
            'success':True,
            'id':n.course_id,
            'course_code':n.course_code,
            'course_name':n.course_name,
            'course_status':n.course_status,
            'course_add_date':n.course_add_date,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def update_course(request):
    course_id = request.POST.get('course_id')
    course_name1 = request.POST.get('course_name1')
    course_code1 = request.POST.get('course_code1')
    try:
        u = osas_r_course.objects.get(course_id = course_id)
        original_course_name = u.course_name 
        orig_course_code = u.course_code 
        if course_name1 and course_code1:
            try:
                u = osas_r_course.objects.get(course_code = course_code1, course_name = course_name1)
                if original_course_name == course_name1:
                    u.course_name = course_name1
                
                if orig_course_code == course_code1:
                    u.course_code = course_code1
                else:
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
                    
                data = {'success':True}
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                u.course_name = course_name1
                u.course_code = course_code1
                u.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
        elif course_name1: 
            try:
                u = osas_r_course.objects.get( course_name = course_name1)
                if original_course_name == course_name1:
                    u.course_name = course_name1
                    # u.save()
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
                else:
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                u.course_name = course_name1
                u.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
        elif course_code1:
            try:
                u = osas_r_course.objects.get( course_code = course_code1)
                if orig_course_code == course_code1:
                    u.course_code = course_code1
                    # u.save()
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
                else:
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                u.course_code = course_code1
                u.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)

    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def deactivate_course(request):
    course_id = request.POST.get("course_id")
    try:
        n = osas_r_course.objects.get(course_id = course_id)
        status_btn = n.course_status
        if status_btn == "ACTIVE":
            status_btn = "INACTIVE"
        else:
            status_btn = "ACTIVE"
        n.course_status = status_btn
        n.save()
        data = {
            'deleted':True,
            'id':n.course_id,
            'course_code':n.course_code,
            'course_name':n.course_name,
            'course_status':n.course_status,
            'course_add_date':n.course_add_date,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)


def add_course(request):
    course_name = request.POST.get('course_name')
    course_code = request.POST.get('course_code')
    try:
        n = osas_r_course.objects.get(course_code = course_code, course_name = course_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        n = osas_r_course(course_code = course_code, course_name = course_name)
        n.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)

#---------------------------------------STUDENT PROFILE--------------------------------------------------------------------------------------------
def student_profile(request):
    txt_course1 = request.POST.get('txt_course')
    txt_yr_sec1 = request.POST.get('yr_sec1')
    txt_Gender1 = request.POST.get('Gender1')
    template_name = 'student/student_profile.html'
    student_info = osas_r_personal_info.objects.order_by('stud_no') 
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    if txt_course1 and txt_yr_sec1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    elif txt_course1 and txt_yr_sec1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec  })
    elif txt_course1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    elif txt_yr_sec1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    elif txt_course1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    elif txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    elif txt_yr_sec1:
        student_info = osas_r_personal_info.objects.all().filter(stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })
    else:
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec })

def student_profile_view(request):
    today = datetime.today()
    student_id = request.POST.get('student_id')
    try:
        d = osas_r_personal_info.objects.get(stud_id = student_id)
      
        student_val = {
            'id':d.stud_id,
            'stud_no':d.stud_no,
            'stud_course_id':d.stud_course_id.course_name,
            'stud_yas_id':d.stud_yas_id.yas_descriptions,
            'stud_lname':d.stud_lname,
            'stud_fname':d.stud_fname,
            'stud_mname':d.stud_mname,
            'stud_sname':d.stud_sname,
            'stud_birthdate':d.stud_birthdate,
            'stud_address':d.stud_address,
            'stud_email':d.stud_email,
            'stud_m_number':d.stud_m_number,
            'stud_hs':d.stud_hs,
            'stud_hs_add':d.stud_hs_add,
            'stud_sh':d.stud_sh,
            'stud_sh_add':d.stud_sh_add,
            'stud_e_name':d.stud_e_name,
            'stud_e_address':d.stud_e_address,
            'stud_e_m_number':d.stud_e_m_number,

        }
        data = {'student_val':student_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:  
        data = {'error':True}
        return JsonResponse(data, safe=False)

  
# Populating 2 dropdown fields in 1 template from the data in 2 different table https://stackoverflow.com/questions/49353000/how-to-have-dropdown-selection-populate-datatables-table-in-template-from-django

def add_student(request):
    template_name = 'student/add_student.html'
    student_course = osas_r_course.objects.order_by('course_name')
    context = {'student_course': student_course}
    student_yr_sec = osas_r_section_and_year.objects.order_by('yas_descriptions')
    context1 = {'student_yr_sec': student_yr_sec}
    return render(request, template_name, {'student_course': student_course, 'student_yr_sec': student_yr_sec})

def student_process_add(request, *args):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    pass1 = request.POST.get('pass1')
    l_name = request.POST.get('stud_lname')
    f_name = request.POST.get('stud_fname')
    m_name = request.POST.get('stud_mname')
    s_name = request.POST.get('stud_sname')
    studno = request.POST.get('stud_no')
    d_of_birth = request.POST.get('stud_birthdate')
    gender = request.POST.get('stud_gender')
    if gender:
        gender = request.POST.get('stud_gender')
    else:
        gender = None
    address = request.POST.get('stud_address')
    email = request.POST.get('stud_email')
    mobile_number = request.POST.get('stud_m_number')
    course = request.POST.get('stud_course')
    yr_sec = request.POST.get('year_sec')
    h_name = request.POST.get('stud_hs')
    h_address = request.POST.get('stud_hs_add')
    sh_name = request.POST.get('stud_sh')
    sh_address = request.POST.get('stud_sh_add')
    e_name = request.POST.get('stud_e_name')
    e_number = request.POST.get('stud_e_m_number')
    e_address = request.POST.get('stud_e_address')
    if pass1:
        stud_pass = pass1
    else:
        stud_pass = randomstr
    try:
        n = osas_r_personal_info.objects.get(stud_no = studno)
        n.stud_lname = request.POST.get('stud_lname')
        n.stud_fname = request.POST.get('stud_fname')
        n.stud_mname = request.POST.get('stud_mname')
        n.stud_sname = request.POST.get('stud_sname')
        n.stud_birthdate = request.POST.get('stud_birthdate')
        n.stud_address = request.POST.get('stud_address')
        n.stud_m_number = request.POST.get('stud_m_number')
        n.stud_email = request.POST.get('stud_email')
        n.stud_hs = request.POST.get('stud_hs')
        n.stud_hs_add = request.POST.get('stud_hs_add')
        n.stud_sh = request.POST.get('stud_sh')
        n.stud_sh_add = request.POST.get('stud_sh_add')
        n.stud_e_name = request.POST.get('stud_e_name')
        n.stud_e_address = request.POST.get('stud_e_address')
        n.stud_e_m_number = request.POST.get('stud_e_m_number')
        if request.POST.get('stud_lname') and request.POST.get('stud_fname') and request.POST.get('stud_mname'):
            n.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        today = datetime.today()
        stud = osas_r_personal_info(
            stud_no = studno, 
            stud_lname = l_name, 
            stud_fname = f_name, 
            stud_mname = m_name, 
            stud_sname = s_name, 
            stud_birthdate = d_of_birth,
            stud_gender = gender, 
            stud_address = address, 
            stud_email = email, 
            stud_m_number = mobile_number, 
            stud_hs = h_name, 
            stud_hs_add = h_address, 
            stud_sh = sh_name, 
            stud_sh_add = sh_address, 
            stud_e_name = e_name,
            stud_e_address = e_address, 
            stud_e_m_number = e_number, 
            s_password = stud_pass , 
            date_created = today, 
            stud_status = 'ACTIVE',
            stud_role = osas_r_userrole.objects.get(user_type='STUDENT'), 
            stud_course_id = osas_r_course.objects.get(course_name = course), 
            stud_yas_id  = osas_r_section_and_year.objects.get(yas_descriptions = yr_sec))
        stud.save()   
        data = {'success':True}
        return JsonResponse(data, safe=False)
       
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
        s = parser.parse(d_of_birth)
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
            student_profile.stud_birthdate = s
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
        if usertype:
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
            return render(request, 'userrole.html')

def deactivate_user(request):
    auth_id = request.POST.get("auth_id")

    try:
        u = osas_r_auth_user.objects.get(auth_id = auth_id, auth_role = osas_r_userrole.objects.get( user_type = "OSAS STAFF"))
        status_btn = u.auth_status
        if status_btn == "ACTIVE":
            status_btn = "INACTIVE"
        else:
            status_btn = "ACTIVE"
        u.auth_status = status_btn
        u.save()
        data = {
            'deleted':True,
            'id':u.auth_id,
            'auth_lname':u.auth_lname,
            'auth_fname':u.auth_fname,
            'auth_username':u.auth_username,
            'auth_password':u.auth_password,
            'auth_role':u.auth_role.user_type,
            'auth_status':u.auth_status,
            'date_created':u.date_created
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def deleteuser(request):
    auth_id = request.POST.get("auth_id")
    try:
        obj = osas_r_auth_user.objects.get(auth_id = auth_id, auth_role = osas_r_userrole.objects.get( user_type = "OSAS STAFF"))
        data = {'deleted':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def auth_user(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    userrole = osas_r_userrole.objects.order_by('user_type')
    template_name = 'auth_user.html'
    if date1 and date2:
        if status:
            auth_user = osas_r_auth_user.objects.all().filter(auth_status = status, date_updated__range=[date1, date2], auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
            return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole})
        else:   
            auth_user = osas_r_auth_user.objects.all().filter(date_updated__range=[date1, date2], auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
            return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole})
    elif status:
        auth_user = osas_r_auth_user.objects.all().filter(auth_status = status, auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
        return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole})
    else:
        auth_user = osas_r_auth_user.objects.all().filter(auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF"), auth_status = "ACTIVE").order_by('-date_updated')
        return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole})
    

def auth_process_edit(request, auth_id):
    template_name = 'auth_process_edit.html'
    role = osas_r_userrole.objects.order_by('user_type')
    try:
        auth_user = osas_r_auth_user.objects.get(auth_id=auth_id)
    except osas_r_auth_user.DoesNotExist:
            raise Http404("User profile does not exist")
    return render(request, template_name,{'auth_user':auth_user, 'role': role})

def auth_edit_user(request):
    auth_id = request.POST.get('auth_id')
    try:
        u = osas_r_auth_user.objects.get(auth_id=auth_id)
        data = {
            'success':True,
            'id':u.auth_id,
            'auth_lname':u.auth_lname,
            'auth_fname':u.auth_fname,
            'auth_username':u.auth_username,
            'auth_password':u.auth_password,
            'auth_role':u.auth_role.user_type,
            'auth_status':u.auth_status,
            'date_created':u.date_created
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def auth_user_update(request):
    auth_id = request.POST.get('user_id')
    user_lname1 = request.POST.get('user_lname1')
    user_fname1 = request.POST.get('user_fname1')
    user_username1 = request.POST.get('user_username1')
    try:
        u = osas_r_auth_user.objects.get(auth_id = auth_id)
        orig_username = u.auth_username 
        if user_username1:
            try:
                u = osas_r_auth_user.objects.get(auth_username = user_username1)
                if orig_username == user_username1:
                    u.auth_lname = user_lname1
                    u.auth_fname = user_fname1
                    u.save()
                else:
                    data = {'error':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                u.auth_username = user_username1
                u.auth_lname = user_lname1
                u.auth_fname = user_fname1
        else:
            u.auth_lname = user_lname1
            u.auth_fname = user_fname1
        u.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def auth_user_edit(request, auth_id):
    auth_user = get_object_or_404(osas_r_auth_user, pk=auth_id)
    try:
        _id = request.POST.get('auth_lname1')
        _lname = request.POST.get('auth_lname1')
        _fname = request.POST.get('auth_fname1')
        _username = request.POST.get('auth_username1')
        _pass = request.POST.get('auth_pass1')
        _pass1 = request.POST.get('auth_pass2')
        _pass2 = request.POST.get('auth_pass3')
        _user = request.POST.get('auth_user1')
        n = osas_r_auth_user.objects.get(auth_id=auth_id)
        if n:
            if _pass:
                if n.auth_password == _pass:
                    if _pass2 or _pass1:
                        if _pass1 == _pass2:
                            if _fname:
                                n.auth_fname = _fname
                            if _lname:
                                n.auth_lname = _lname
                            if _pass2: 
                                n.auth_password = _pass2
                            if _user:
                                crs = osas_r_userrole.objects.get(user_type=_user)        
                                n.auth_role = crs
                                n.save()
                                messages.success(request, _username + ' ' +  'Successfully Updated!')
                                return redirect('auth_user')
                        else:
                            messages.error(request, 'Password does not match!')
                            return HttpResponseRedirect(reverse('auth_process_edit', args=(auth_id,))) 
                    else:
                        messages.error(request, 'Please enter new password.')
                        return HttpResponseRedirect(reverse('auth_process_edit', args=(auth_id,))) 
                else:
                    messages.error(request, 'Incorrect old password.')
                    return HttpResponseRedirect(reverse('auth_process_edit', args=(auth_id,))) 
            else:
                if _fname:
                    n.auth_fname = _fname
                if _lname:
                    n.auth_lname = _lname
                if _user:
                    crs = osas_r_userrole.objects.get(user_type=_user)        
                    n.auth_role = crs
            n.save()
            messages.success(request, str(_username) + ' ' +  'Successfully Updated!')
            return HttpResponseRedirect(reverse('auth_process_edit', args=(auth_id,)))             
        else:
            messages.error(request, 'Problem updating record')
            return render(request, 'auth_user.html')
    except (KeyError, osas_r_auth_user.DoesNotExist ):
        messages.error(request, 'Problem updating record')
        return render(request, 'auth_user.html')
        
def auth_user_add(request):
    _lname = request.POST.get('user_lname')
    _fname = request.POST.get('user_fname')
    _username = request.POST.get('user_username')
    _pass = request.POST.get('user_password')
    _pass1 = request.POST.get('user_password1')
    try:
        n = osas_r_auth_user.objects.get(auth_username = _username)
        data = {'error' :True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        today = datetime.today()
        u = osas_r_auth_user.objects.create(auth_lname=_lname,auth_fname=_fname, auth_username=_username, auth_password=_pass, auth_role = osas_r_userrole.objects.get(user_type= "OSAS STAFF"), date_created=today)
        u.save()

        data = {
            'id':u.auth_id,
            'auth_lname':u.auth_lname,
            'auth_fname':u.auth_fname,
            'auth_username':u.auth_username,
            'auth_password':u.auth_password,
            'auth_role':u.auth_role.user_type,
            'auth_status':u.auth_status,
            'date_created':u.date_created
        }
        return JsonResponse(data, safe=False)

    
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
        if usertype:
            user_profile.user_type = usertype
        user_profile.date_updated = today
        user_profile.save()
        return HttpResponseRedirect('/userrole' , {'success_message': "Congratulations," })

def adduserrole(request):
    usertype = request.POST.get('userrole1')
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
            return render(request, 'userrole.html')

def deleteuser(request):
    id = request.POST.get('del_user_id')
    osas_r_userrole.objects.get(pk=id).delete()
    return HttpResponseRedirect('/userrole')

#------------------------------------PROFILE------------------------------------------------------------
def profile(request):
    template_name = 'Role_Student/profile.html'
    request.session['session_user_id']
    request.session['session_user_no']
    try:
        profile = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])
        s = profile.stud_birthdate
        n = datetime.strptime(str(s), "%Y-%m-%d").date()
        return render(request, template_name, {'profile': profile, 'n': n})
    except ObjectDoesNotExist:
        return render(request, 'Role_Student/profile.html')
    
def student_profile_edit(request):
    request.session['session_user_id']
    request.session['session_user_no']
    course = request.POST.get('txt_course')
    yr_sec = request.POST.get('txt_yr_sec')
    try:
        student_profile = osas_r_personal_info.objects.get(stud_id=request.session['session_user_id'])
        l_name = request.POST.get('txt_l_name')
        f_name = request.POST.get('txt_f_name')
        m_name = request.POST.get('txt_m_name')
        s_name = request.POST.get('txt_s_name')
        studno = request.POST.get('txt_studno')
        d_of_birth = request.POST.get('date_of_birth')
        if d_of_birth:
            s = parser.parse(d_of_birth)
        gender = request.POST.get('txt_Gender')
        address = request.POST.get('txt_address')
        email = request.POST.get('txt_email')
        mobile_number = request.POST.get('txt_mobile_number')
        course = request.POST.get('txt_course')
        yr_sec = request.POST.get('txt_yr_sec')
        h_name = request.POST.get('txt_h_name')
        h_address = request.POST.get('txt_h_address')
        sh_name = request.POST.get('txt_sh_name')
        sh_address = request.POST.get('txt_sh_address')
        sh_name = request.POST.get('txt_sh_name')
        sh_address = request.POST.get('txt_sh_address')
        e_name = request.POST.get('txt_e_name')
        e_number = request.POST.get('txt_e_number')
        e_address = request.POST.get('txt_e_address')
    except ObjectDoesNotExist:
        messages.error(request, 'Invalid Student Number')
        return render(request, 'student/student_profile.html')
    else: # passing the value from template to database
        today = datetime.today()
        student_profile = osas_r_personal_info.objects.get(stud_id=request.session['session_user_id'])
        if studno:
            student_profile.stud_no = studno
        if d_of_birth:
            # datebirth = datetime.strptime(d_of_birth, '%B %d, %Y')
            student_profile.stud_birthdate = s
        if yr_sec:
            year_sec = osas_r_section_and_year.objects.get(yas_descriptions=yr_sec)
            student_profile.stud_yas_id = year_sec
        if course:
            crs = osas_r_course.objects.get(course_name=course)
            student_profile.stud_course_id = crs
        student_profile.stud_lname = l_name
        student_profile.stud_fname = f_name
        student_profile.stud_mname = m_name
        if gender:
            student_profile.stud_gender = gender
        student_profile.stud_sname = s_name
        student_profile.stud_address = address
        student_profile.stud_email = email
        student_profile.stud_m_number = mobile_number
        student_profile.stud_hs = h_name
        student_profile.stud_hs_add = h_address
        student_profile.stud_e_name = e_name
        student_profile.stud_e_address = e_address
        student_profile.stud_e_m_number = e_number
        student_profile.stud_sh = sh_name
        student_profile.stud_sh_add = sh_address
        student_profile.date_updated = today
        student_profile.save()
        return HttpResponseRedirect('/profile')

    
def organization_student_data(request):
    selected_student = request.POST.get('selected_student')
    try:
        t = osas_r_personal_info.objects.get(stud_no = selected_student)
        data = {
            'lname': t.stud_lname,
            'fname': t.stud_fname,
            'mname': t.stud_mname,
            'sname': t.stud_sname,
            'course': t.stud_course_id.course_name,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'Facilitation/organization.html')

def classroom_student_data(request):
    stud_course = request.POST.get('stud_course')
    stud_year_sec = request.POST.get('stud_year_sec')
    if stud_course == 'N/A':
        stud_list = list(osas_r_personal_info.objects.all().values())
    else:
        stud_list = list(osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = stud_course), stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = stud_year_sec)).values())
    return JsonResponse({
        'data': stud_list,
    })

def organization_student(request):
    org_info = organization.objects.all().filter(org_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']))
    return render(request, 'Role_Student/organization.html', {'org_info':org_info})
  
def organization_osas(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    stud_list = osas_r_personal_info.objects.all().order_by("stud_no")
    year = str(acad_year)

    course_list =  osas_r_course.objects.all().order_by("course_name")
    year_sec_list = osas_r_section_and_year.objects.all().order_by("-yas_descriptions")
    if acad_year and status:
        org_list = organization.objects.all().filter(org_status = status, org_datecreated__contains =  year).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    elif acad_year:
        org_list = organization.objects.all().filter(org_datecreated__contains =  year).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    elif status:
        org_list = organization.objects.all().filter(org_status = status ).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    else:   
        org_list = organization.objects.all().order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
        
def organization_osas_classroom(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    stud_list = osas_r_personal_info.objects.all().order_by("stud_no")
    year = str(acad_year)

    course_list =  osas_r_course.objects.all().order_by("course_name")
    year_sec_list = osas_r_section_and_year.objects.all().order_by("-yas_descriptions")
    if acad_year and status:
        org_list = classroom.objects.all().filter(room_status = status, room_datecreated__contains =  year).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    elif acad_year:
        org_list = classroom.objects.all().filter(room_datecreated__contains =  year).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    elif status:
        org_list = classroom.objects.all().filter(room_status = status ).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})
    else:   
        org_list = classroom.objects.all().order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list, 'course_list':course_list, 'year_sec_list':year_sec_list})


def organization_osas_new_class_account(request):
    stud = request.POST.get('stud')
    class_year = request.POST.get('class_year')
    class_course = request.POST.get('class_course')
    class_email = request.POST.get('class_email')
    class_pass = request.POST.get('class_pass')
    adviser = request.POST.get('stud_adviser')
    try:
        c = classroom.objects.get(room_course = class_course, room_year = class_year)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        try:
            o = officer.objects.get(off_stud_id = osas_r_personal_info.objects.get(stud_no = stud), off_position = 'President')
            data = {'error1':True} 
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            try: 
                c = classroom.objects.get(room_email = class_email)
                data = {'error2':True} 
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                try:
                    p = organization.objects.get(org_email = class_email)
                    data = {'error2':True} 
                    return JsonResponse(data, safe=False)
                except ObjectDoesNotExist:
                    today = datetime.today()
                    year = timedelta(days=365)
                    room_datecreated = today
                    room_expiration = today + year
                    room = classroom( 
                        room_year = class_year,
                        room_course = class_course, 
                        room_email = class_email, 
                        room_pass = class_pass, 
                        room_stud_id = osas_r_personal_info.objects.get(stud_no = stud), 
                        room_datecreated = room_datecreated,
                        room_expiration = room_expiration,
                        room_adviser = adviser
                        )
                    room.save()
                    officer.objects.create(
                        off_stud_id = osas_r_personal_info.objects.get(stud_no = stud),
                        off_room_id = classroom.objects.get(room_stud_id = osas_r_personal_info.objects.get(stud_no = stud)), 
                        off_position = 'President')
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                

def organization_new_account(request):
    stud = request.POST.get('stud')
    org_name = request.POST.get('org_name')
    org_type = request.POST.get('org_type')
    org_adviser = request.POST.get('org_adviser')
    class_course = request.POST.get('class_course')
    org_abbr = request.POST.get('org_abbr')
    org_email = request.POST.get('org_email')
    org_pass = request.POST.get('org_pass')
    print(org_name, org_abbr, org_email, org_pass, stud)
    if class_course == 'N/A':
        try:
            c = organization.objects.get(org_name = org_name)
            data = {'error':True}
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            try:
                o = officer.objects.get(off_stud_id = osas_r_personal_info.objects.get(stud_no = stud), off_position = 'President')
                data = {'error1':True} 
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                try: 
                    c = classroom.objects.get(room_email = org_email)
                    data = {'error2':True} 
                    return JsonResponse(data, safe=False)
                except ObjectDoesNotExist:
                    try:
                        p = organization.objects.get(org_email = org_email)
                        data = {'error2':True} 
                        return JsonResponse(data, safe=False)
                    except ObjectDoesNotExist:
                        today = datetime.today()
                        year = timedelta(days=365)
                        org_date_accredited = today
                        org_expiration = today + year
                        room = organization( 
                            org_name = org_name,
                            org_abbr = org_abbr, 
                            org_email = org_email, 
                            org_pass = org_pass, 
                            org_type = org_type,
                            org_adviser = org_adviser,
                            org_stud_id = osas_r_personal_info.objects.get(stud_no = stud), 
                            org_expiration = org_expiration,
                            org_status = 'INACTIVE',
                            org_course = class_course
                            )
                        room.save()
                        officer.objects.create(
                            off_stud_id = osas_r_personal_info.objects.get(stud_no = stud),
                            off_org_id = organization.objects.get(org_stud_id = osas_r_personal_info.objects.get(stud_no = stud)), 
                            off_position = 'President')
                        data = {'success':True}
                        return JsonResponse(data, safe=False)
    else:
        try:
            c = organization.objects.get(org_name = org_name)
            data = {'error':True}
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            try:
                o = officer.objects.get(off_stud_id = osas_r_personal_info.objects.get(stud_no = stud), off_position = 'President')
                data = {'error1':True} 
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                try: 
                    c = classroom.objects.get(room_email = org_email)
                    data = {'error2':True} 
                    return JsonResponse(data, safe=False)
                except ObjectDoesNotExist:
                    try:
                        p = organization.objects.get(org_email = org_email)
                        data = {'error2':True} 
                        return JsonResponse(data, safe=False)
                    except ObjectDoesNotExist:
                        today = datetime.today()
                        year = timedelta(days=365)
                        org_date_accredited = today
                        org_expiration = today + year
                        room = organization( 
                            org_name = org_name,
                            org_abbr = org_abbr, 
                            org_email = org_email, 
                            org_pass = org_pass, 
                            org_type = org_type,
                            org_adviser = org_adviser,
                            org_stud_id = osas_r_personal_info.objects.get(stud_no = stud), 
                            org_expiration = org_expiration,
                            org_status = 'INACTIVE'
                            )
                        room.save()
                        officer.objects.create(
                            off_stud_id = osas_r_personal_info.objects.get(stud_no = stud),
                            off_org_id = organization.objects.get(org_stud_id = osas_r_personal_info.objects.get(stud_no = stud)), 
                            off_position = 'President')
                        data = {'success':True}
                        return JsonResponse(data, safe=False)

def organization_update_account(request):
    stud = request.POST.get('stud')
    org_id = request.POST.get('org_id')
    org_name = request.POST.get('org_name')
    org_abbr = request.POST.get('org_abbr')
    org_email = request.POST.get('org_email')
    org_pass = request.POST.get('org_pass')
    today = datetime.today()
    try:
        org = organization.objects.get(org_id = org_id)
        student = osas_r_personal_info.objects.get(stud_no = stud)
        org.org_name = org_name
        org.org_email = org_email
        org.org_pass = org_pass
        org.org_abbr = org_abbr
        org.org_stud_id = osas_r_personal_info.objects.get(stud_id = student.stud_id)
        org.org_dateupdated = today
        org.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def classroom_update_account(request):
    stud = request.POST.get('stud')
    room_id = request.POST.get('room_id')
    room_email = request.POST.get('room_email')
    room_pass = request.POST.get('room_pass')
    today = datetime.today()
    try:
        room = classroom.objects.get(room_id = room_id)
        student = osas_r_personal_info.objects.get(stud_no = stud)
        room.room_email = room_email
        room.room_pass = room_pass
        room.room_stud_id = osas_r_personal_info.objects.get(stud_id = student.stud_id)
        room.room_dateupdated = today
        room.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_status_account(request):
    org_id = request.POST.get('org_id')
    org_status = request.POST.get('status')
    today = datetime.today()
    year = timedelta(days=365)
    org_date_accredited = today
    org_date_accredited_year = today
    org_expiration = today + year
    try:
        org = organization.objects.get(org_id = org_id)
        if org_status == 'Dismiss':
            org.org_status = 'DISMISSED'
            org.org_date_accredited = None
            org.org_expiration = None
            org.org_date_accredited_year = None
            org.org_submit_date = None
            org.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
        else:
            org.org_status = 'ACCREDITED'
            org.org_date_accredited = today
            org.org_date_accredited_year = today
            org.org_expiration = today + year
            org.org_submit_date = today
            org.org_accre_status = org.org_accre_status + 1
            org.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_accreditation(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    acc_docu_list = org_accreditation.objects.all().filter(acc_status = 'SENT')
    acc_docu = org_accreditation.objects.all().order_by("acc_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        acc_list = organization.objects.all().filter(org_status = status, org_date_accredited__contains = year).order_by("-org_date_accredited")
        return render(request, 'Facilitation/accreditation.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg})
    elif acad_year:
        acc_list = organization.objects.all().filter(org_date_accredited__contains = year).order_by("-org_date_accredited")
        return render(request, 'Facilitation/accreditation.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg})
    if status:
        acc_list = organization.objects.all().filter(org_status = status ).order_by("-org_date_accredited")
        return render(request, 'Facilitation/accreditation.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg})
    else:
        acc_list = organization.objects.all().order_by("-org_date_accredited")   
        return render(request, 'Facilitation/accreditation.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg})
        
   
def organization_accreditation_expired(request):
    org_list = list(organization.objects.values())
    return JsonResponse({'data': org_list})

def organization_expired(request):
    org_id = request.POST.get('org_id')
    org_date = request.POST.get('org_date')
    try: 
        o = organization.objects.get(org_id = org_id)
        if o.org_date_accredited == o.org_expiration:     
            o.org_status = "INACTIVE"
            o.org_accre_status = 1
            o.org_submit_date = None
            o.org_date_accredited = None
            o.org_date_accredited_year = None
            o.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
        return HttpResponse('')
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_addnnote(request):
    org_id = request.POST.get('org_id')
    org_note = request.POST.get('sample')

    try:
        d = organization.objects.get(org_id = org_id)
        d.org_notes = org_note
        d.save()
        data = {'success':True,
        'id': d.org_id
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_approve(request):
    org_id = request.POST.get('org_id')
    org_term = request.POST.get('org_term')
    try:
        d = organization.objects.get(org_id = org_id)
        d.org_status = 'ACCREDITED'
        today = datetime.today()
        year = timedelta(days=365)
        d.org_date_accredited = today
        d.org_date_accredited_year = today
        d.org_expiration = today + year
        d.save()
        data = {'success':True,
        'id': d.org_id
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def concept_paper_validate(request):
    title_id = request.POST.get('title_id')
    stats = request.POST.get('stats')
    today = datetime.today()
    try:
        d = concept_paper_title.objects.get(title_id = title_id)
        if stats == "PENDING":
            d.title_status = 'VALIDATED'
            d.save()
        else:
            d.title_status = 'APPROVED'
            d.title_dateapproved = today
            d.save()
        data = {'success':True,
        'id': d.title_id
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_view_messages(request):
    org_id = request.POST.get('org_id')
    messages_list = list(organization_chat.objects.all().values())
    org_id = organization.objects.get(org_id = org_id)
    osas_role = osas_r_auth_user.objects.get(auth_role = osas_r_userrole.objects.get(user_type = "HEAD OSAS"))
    osas_id = osas_r_auth_user.objects.get(auth_id = osas_role.auth_id)
   
    return JsonResponse({
        'data': messages_list,
        'org_data':org_id.org_abbr,
        'org_id':org_id.org_abbr,
        'org_msg_status':org_id.org_abbr,
        'osas_data':osas_id.auth_role.user_type,
        'osas_role_id':osas_role.auth_id,
        'osas_role':osas_role.auth_role.user_type,
    })

def class_view_messages(request):
    room_id = request.POST.get('room_id')
    messages_list = list(organization_chat.objects.all().values())
    room_id = classroom.objects.get(room_id = room_id)
    osas_role = osas_r_auth_user.objects.get(auth_role = osas_r_userrole.objects.get(user_type = "HEAD OSAS"))
    osas_id = osas_r_auth_user.objects.get(auth_id = osas_role.auth_id)
   
    return JsonResponse({
        'data': messages_list,
        'room_id':room_id.room_id,
        'room_year':room_id.room_year,
        'room_sec':room_id.room_sec,
        'room_course':room_id.room_stud_id.stud_course_id.course_name,
        'osas_data':osas_id.auth_role.user_type,
        'osas_role_id':osas_role.auth_id,
        'osas_role':osas_role.auth_role.user_type,
    })

def organization_osas_msg_seen(request):
    osas_message = request.POST.get('osas_message')
    try:
        osas = organization_chat.objects.get(msg_id = osas_message)
        osas.msg_status = "Seen"
        osas.save()
        data = {'osas_msg_status':osas.msg_status}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_msg_clear(request):
    msg_id = request.POST.get('msg_id')
    try:
        d = organization_chat.objects.get(msg_id = msg_id)
        d.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_view_document(request):
    org_id = request.POST.get('org_id')
    try:
        d = organization.objects.get(org_id = org_id)
        data = { 'id': d.org_id,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_upload_osas(request):
    pk_id = request.POST.get('pk_id')
    ident = request.POST.get('identity')
    docu = request.FILES.get('file')
    title_id = request.POST.get('title_id')
    auth_id = request.session['session_user_id']
    filename = str(docu)
    extension = filename.split(".")[1]
    if request.method == 'POST':
        if ident == 'org':
            try:
                o = org_concept_paper.objects.get(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_file = docu, con_org_id = organization.objects.get(org_id = pk_id))
                o.delete()
                org_concept_paper.objects.create(con_file = docu, con_org_id = organization.objects.get(org_id = pk_id), con_file_ext = extension, con_status = "APPROVED", con_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), con_title_id = concept_paper_title.objects.get(title_id = title_id))
                return HttpResponse('')
            except ObjectDoesNotExist:
                org_concept_paper.objects.create(con_file = docu, con_org_id = organization.objects.get(org_id = pk_id), con_file_ext = extension, con_status = "APPROVED", con_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), con_title_id = concept_paper_title.objects.get(title_id = title_id))
                return HttpResponse('')
        elif ident == 'class':
            
            try:
                o = org_concept_paper.objects.get(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_file = docu, con_room_id = classroom.objects.get(room_id = pk_id))
                o.delete()
                org_concept_paper.objects.create(con_file = docu, con_room_id = classroom.objects.get(room_id = pk_id), con_file_ext = extension, con_status = "APPROVED" , con_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), con_title_id = concept_paper_title.objects.get(title_id = title_id))
                print('room_id = '+ pk_id, ' type = ' + ident, 'title_id = ' + title_id, docu)
            except ObjectDoesNotExist:
                print('room_id = '+ pk_id, ' type = ' + ident, 'title_id = ' + title_id, docu, 'error')
                return HttpResponse('')
    return JsonResponse({'error': True})

def organization_view_certificate(request):
    org_id = request.POST.get('org_id')
    try:
        c = organization.objects.get(org_id = org_id)
        org_val = {
            "org_id":c.org_id, 
            "org_name":c.org_name, 
            'org_email':c.org_email, 
            'org_abbr':c.org_abbr, 
            'org_date_accredited':c.org_date_accredited, 
            'org_datecreated':c.org_datecreated, 
        }
        data = {'org_val':org_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def organization_generate_report(request):
    date_from = request.POST.get('from_2')
    date_to = request.POST.get('to_2')
    try:    
        accredited_values = list(organization.objects.all().filter(org_date_accredited_year__range = [date_from, date_to], org_status = "ACCREDITED").values())
        return JsonResponse({'data': accredited_values})
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def event_generate_report(request):
    date_from = request.POST.get('from_2')
    date_to = request.POST.get('to_2')
    try:    
        accredited_values = list(concept_paper_title.objects.all().filter(title_datecreated__range = [date_from, date_to]).values().order_by('title_datecreated'))
        accredited_values2 = concept_paper_title.objects.all().filter(title_datecreated__range = [date_from, date_to]).values().order_by('title_datecreated')

        return JsonResponse({
            'data': accredited_values,
        })
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def event_accomplishment_report(request):
    date_from = request.POST.get('from_2')
    date_to = request.POST.get('to_2')
    try:    
        accredited_values = list(concept_paper_title.objects.all().filter(title_date_accomplished__range = [date_from, date_to], title_status = "ACCOMPLISHED").values().order_by('title_date_accomplished'))
        return JsonResponse({
            'data': accredited_values,
        })
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def organization_dismiss(request):
    org_id = request.POST.get('org_id')
    try:
        d = organization.objects.get(org_id = org_id)
        d.org_status = 'DISMISSED'
        d.org_date_accredited = None
        d.org_expiration = None
        d.org_date_accredited_year = None
        d.save()
        data = {'success':True,
        'id': d.org_id
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_login(request):
    return render(request, 'Organization/login.html')

def organization_home(request):
    total_balance = organization.objects.get(org_id = request.session['session_user_id'])
    total_event = concept_paper_title.objects.filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id'])).count()
    total_accomplished = concept_paper_title.objects.filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id']), title_status = 'ACCOMPLISHED').count()
    return render(request, 'Organization/home.html',{'total_balance':total_balance, 'total_event':total_event, 'total_accomplished':total_accomplished})

def organization_changepass_verify(request):
    old_password = request.POST.get('old_pass')
    try:
        o = organization.objects.get(org_id = request.session['session_user_id'], org_pass = old_password)
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)

def organization_changepass(request):
    new_pass = request.POST.get('new_pass')
    try:
        o = organization.objects.get(org_id = request.session['session_user_id'])
        o.org_pass = new_pass
        o.save()
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)


def classroom_home(request):
    total_balance = classroom.objects.get(room_id = request.session['session_user_id'])
    total_event = concept_paper_title.objects.filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id'])).count()
    total_accomplished = concept_paper_title.objects.filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id']), title_status = 'ACCOMPLISHED').count()
    return render(request, 'classroom/home.html',{'total_balance':total_balance, 'total_event':total_event, 'total_accomplished':total_accomplished})

def classroom_changepass_verify(request):
    old_password = request.POST.get('old_pass')
    try:
        o = classroom.objects.get(room_id = request.session['session_user_id'], room_pass = old_password)
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)

def classroom_changepass(request):
    new_pass = request.POST.get('new_pass')
    try:
        o = classroom.objects.get(room_id = request.session['session_user_id'])
        o.room_pass = new_pass
        o.save()
        data = {'success':True} 
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True} 
        return JsonResponse(data, safe=False)

def organiation_login_process(request):
    s_no = request.POST.get('stud_no')
    password = request.POST.get('pass')
    try:
        c = organization.objects.get(org_email=s_no)
        org = organization.objects.filter(org_email=s_no, org_pass= password)
        if org:
            request.session['session_user_id'] = c.org_id
            request.session['session_user_no'] = c.org_email
            request.session['session_user_role'] = c.org_name
            request.session['session_org_abbr'] = c.org_abbr
            value_list = organization_chat.objects.filter(msg_status = 'Delevired', msg_send_to = request.session['session_org_abbr']).count()
            return HttpResponseRedirect('/organization_home', {'value_list':value_list})
        else:
            messages.error(request, 'Either email address or password are incorrect.')
            return HttpResponseRedirect('/organization_login')
    except ObjectDoesNotExist:
        messages.error(request, 'Invalid email address, please try again.')
        return HttpResponseRedirect('/organization_login')

def organization_logout(request):
    try:
        del request.session['session_user_role']
        request.session['session_user_role'] = 'none'
        return render(request, 'Organization/login.html', {})
    except KeyError:
        return render(request, 'Organization/login.html', {})

def osas_accreditation_requirements(request):
    acad_year = request.POST.get('acad_year')
    org_term = request.POST.get('org_term')
    org_id = request.POST.get('org_id')
    today = datetime.today()
    if acad_year:
        year = str(acad_year)
        year2 = str(today.year)
    
    o = organization.objects.get(org_id = org_id)
    orgname = o.org_name
    org_docu = list(org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = org_id), acc_docu_term = org_term).values())
    #New
    if org_term == '0':
        return JsonResponse({
        'data': org_docu,
        'orgname':o.org_abbr,
        'orgstatus':o.org_status,
        'org_submit_date':o.org_submit_date,
        'org_accre_status':o.org_accre_status,
        'org_date_accredited':o.org_date_accredited,
        'org_type':o.org_type,
        'org_adviser':o.org_adviser
        })
    #Renew    
    elif org_term == '1':
        return JsonResponse({
        'data': org_docu,
        'orgname':o.org_abbr,
        'orgstatus':o.org_status,
        'org_submit_date':o.org_submit_date,
        'org_accre_status':o.org_accre_status,
        'org_date_accredited':o.org_date_accredited,
        'org_type':o.org_type,
        'org_adviser':o.org_adviser
        })
    else:
        data = {'error':True} 
        return JsonResponse(data, safe=False)
    

def accreditation(request):
    acad_year = request.POST.get('acad_year')
    today = datetime.today()
    year = str(acad_year)
    year2 = str(today.year)
    d = organization.objects.get(org_id = request.session['session_user_id'])
    org_id = d.org_id
    org_term = d.org_accre_status
    org_type = d.org_type
    org_status = d.org_status
    print(org_status)
    o = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_docu_term = org_term)
    if org_term <= 0:
        docu_type = ['Constitutions and By Laws','Set of Officers','One-year Plan of Activities','Financial Clearance','Clearance/Certificate (College-Based)','Clearance/Certificate (University-Wide)','Guidance Certificate','Medical Certificate','Registrar Certificate']
        for x in o:
            if x.acc_title in docu_type:
                p = docu_type.index(x.acc_title)
                print(docu_type.index(x.acc_title))
                del docu_type[p]
    elif org_term > 0:
        docu_type = ['Annual Report','Financial Statement','New Constitution','Set of Officers','Plan Activities','Clearance/Certificate (College-Based)','Clearance/Certificate (University-Wide)','Audit Clearance','Guidance Certificate','Medical Certificate','Registrar Certificate']
        for x in o:
            if x.acc_title in docu_type:
                p = docu_type.index(x.acc_title)
                print(docu_type.index(x.acc_title))
                del docu_type[p]
    if acad_year:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_datecreated__contains = year, acc_docu_term = org_term).order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'org_term':org_term, 'docu_type':docu_type, 'org_type':org_type, 'org_status':org_status, 'org_id':org_id})
    else:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_datecreated__contains = year2, acc_docu_term = org_term).order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'org_term':org_term, 'docu_type':docu_type, 'org_type':org_type, 'org_status':org_status, 'org_id':org_id})

def accreditation_upload(request):
    docu = request.FILES.get('file')
    docu_type = request.POST.get('docu_type')
    docu_id = request.POST.get('docu_id')
    filename = str(docu)
    extension = filename.split(".")[1]
    if request.method == 'POST':
        try:
            o = organization.objects.get(org_id = request.session['session_user_id'])
            term = o.org_accre_status
            if docu_id:
                try:
                    p = org_accreditation.objects.get(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_id = docu_id)
                    p.delete()
                    org_accreditation.objects.create(acc_title = docu_type, acc_file =  docu, acc_doc_type =  extension, acc_docu_term = term, acc_org_id = organization.objects.get(org_id = request.session['session_user_id']))
                    return HttpResponse('')
                except ObjectDoesNotExist:
                    org_accreditation.objects.create(acc_title = docu_type, acc_file =  docu, acc_doc_type =  extension, acc_docu_term = term, acc_org_id = organization.objects.get(org_id = request.session['session_user_id']))
                    return HttpResponse('')
            else:
                org_accreditation.objects.create(acc_title = docu_type, acc_file =  docu, acc_doc_type =  extension, acc_docu_term = term, acc_org_id = organization.objects.get(org_id = request.session['session_user_id']))
                return HttpResponse('')
        except ObjectDoesNotExist:
            return JsonResponse({'error': True})
    return JsonResponse({'error': True})

def accreditation_document_remove(request):
    doc_id = request.POST.get('acc_id')
    try:
        d = org_accreditation.objects.get(acc_id = doc_id)
        d.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_sending_files(request):
    docu_ids = request.POST.getlist('docu_ids[]')
    today = datetime.today()
    str_list = list(filter(None, docu_ids))
    for x in str_list:
        print(int(x))
        try:
            d = org_accreditation.objects.get(acc_id = x)
            d.acc_status = 'SENT'
            d.acc_issue = None
            o = organization.objects.get(org_id = request.session['session_user_id'])
            o.org_submit_date = today
            o.org_issue = None
            o.save()
            d.save()
        except ObjectDoesNotExist:
            data = {'error':True}
            return JsonResponse(data, safe=False)
    data = {'success':True}
    return JsonResponse(data, safe=False)
   

def accreditation_document_return(request):
    doc_id = request.POST.get('acc_id')
    org_id = request.POST.get('org_id')
    try:
        d = org_accreditation.objects.get(acc_id = doc_id)
        e = organization.objects.get(org_id = org_id)
        if e.org_status == 'ACCREDITED':
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d.acc_status = "SAVED"
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def org_concept_paper_document_return(request):
    con_id = request.POST.get('con_id')
    org_id = request.POST.get('org_id')
    try:
        d = org_concept_paper.objects.get(con_id = con_id)
        if d.con_title_id.title_status == "VALIDATED":
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d.con_status = "SAVED"
            d.con_title_id = None
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def class_concept_paper_document_return(request):
    con_id = request.POST.get('con_id')
    room_id = request.POST.get('room_id')
    try:
        d = org_concept_paper.objects.get(con_id = con_id)
        e = classroom.objects.get(room_id = room_id)
        if d.con_title_id.title_status == "VALIDATED":
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d.con_status = "SAVED"
            d.con_title_id = None
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_document_send(request):
    doc_id = request.POST.get('doc_id')
    org_id = request.POST.get('org_id')
    today = datetime.today()
    try:
        d = org_accreditation.objects.get(acc_id = doc_id)
        g = organization.objects.get(org_id = org_id)
        if g.org_status == 'ACCREDITED':
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d.acc_status = "SENT"
            e = organization.objects.get(org_id = request.session['session_user_id'])
            e.org_submit_date = today
            e.save()
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)


def class_concept_paper_send(request):
    doc_id = request.POST.get('doc_id')
    title_name = request.POST.get('con_title')
    room_id = request.POST.get('room_id')
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        if t.title_status == "VALIDATED" or t.title_status == "APPROVED" :
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d = org_concept_paper.objects.get(con_id = doc_id)
            g = classroom.objects.get(room_id = room_id)
            d.con_status = "SENT"
            d.con_title_id = concept_paper_title.objects.get(title_name = title_name)
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_status = "PENDING", title_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
        d = org_concept_paper.objects.get(con_id = doc_id)
        d.con_title_id = concept_paper_title.objects.get(title_name = title_name)
        d.con_status = "SENT"
        d.save()
        data = {'error':True}
        return JsonResponse(data, safe=False)

def class_concept_paper_title(request):
    title_name = request.POST.get('con_title')
    room_id = request.POST.get('room_id')
    date_conducted = request.POST.get('date_conducted')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    serial_no = 'SN-' + randomstr
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name,  title_serial = serial_no, title_status = "PENDING", title_room_id = classroom.objects.get(room_id = room_id), title_date_conducted = date_conducted)
        data = {'success':True}
        return JsonResponse(data, safe=False)
        
def org_concept_paper_send(request):
    doc_id = request.POST.get('doc_id')
    title_name = request.POST.get('con_title')
    org_id = request.POST.get('org_id')
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        if t.title_status == "VALIDATED" or t.title_status == "APPROVED" :
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            d = org_concept_paper.objects.get(con_id = doc_id)
            d.con_status = "SENT"
            d.con_title_id = concept_paper_title.objects.get(title_name = title_name)
            d.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_status = "PENDING", title_org_id = organization.objects.get(org_id = request.session['session_user_id']))
        d = org_concept_paper.objects.get(con_id = doc_id)
        d.con_title_id = concept_paper_title.objects.get(title_name = title_name)
        d.con_status = "SENT"
        d.save()
        data = {'error':True}
        return JsonResponse(data, safe=False)

def org_concept_paper_title(request):
    title_name = request.POST.get('con_title')
    date_conducted = request.POST.get('date_conducted')
    org_id = request.POST.get('org_id')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    serial_no = 'SN-' + randomstr
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_serial = serial_no, title_status = "PENDING", title_org_id = organization.objects.get(org_id = org_id), title_date_conducted = date_conducted)
        data = {'success':True}
        return JsonResponse(data, safe=False)

def accreditation_document_return_osas(request):
    doc_id = request.POST.get('id')
    today = datetime.today()
    try:
        d = org_accreditation.objects.get(acc_id = doc_id)
        d.acc_status = 'SAVED'
        d.acc_datesubmitted = None
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_document_sent(request):
    doc_id = request.POST.get('id')
    docu_type = request.POST.get('docu_type')
    today = datetime.today()
    try:
        d = org_accreditation.objects.get(acc_id = doc_id, acc_title = docu_type)
        d.acc_status = 'SENT'
        d.acc_datesubmitted = today
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_document_delete(request):
    doc_id = request.POST.get('id')
    docu_type = request.POST.get('docu_type')
    try:
        d = org_accreditation.objects.get(acc_id = doc_id, acc_title = docu_type)
        d.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def org_concept_paper_document_delete(request):
    doc_id = request.POST.get('doc_id')
    org_id = request.POST.get('org_id')
    btn_status = request.POST.get('btn_status')
    try:
        d = org_concept_paper.objects.get(con_id = doc_id)
        if btn_status == "Remove File(s)":
            d.delete()
        elif btn_status == "Retrieve File(s)":
            if d.con_title_id.title_status == "VALIDATED":
                data = {'error':True}
                return JsonResponse(data, safe=False)
            elif d.con_title_id.title_status == "APPROVED":
                data = {'error':True}
                return JsonResponse(data, safe=False)
            else:
                d.con_status = "SAVED"
                d.con_title_id = None
                d.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def class_concept_paper_document_delete(request):
    doc_id = request.POST.get('doc_id')
    room_id = request.POST.get('room_id')
    btn_status = request.POST.get('btn_status')
    try:
        d = org_concept_paper.objects.get(con_id = doc_id)
        if btn_status == "Remove File(s)":
            d.delete()
        elif btn_status == "Retrieve File(s)":
            if d.con_title_id.title_status == "VALIDATED":
                data = {'error':True}
                return JsonResponse(data, safe=False)
            elif d.con_title_id.title_status == "APPROVED":
                data = {'error':True}
                return JsonResponse(data, safe=False)
            else:
                d.con_status = "SAVED"
                d.con_title_id = None
                d.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_osas_msg(request):
    organization_id = request.POST.get('organization_id')
    osas_id = request.POST.get('osas_id')
    btn_status = request.POST.get('msg')
    date_today = request.POST.get('date_today')
    s = organization.objects.get(org_id = organization_id)
    s.org_abbr
    try:
        today = datetime.today()
        d = organization_chat(
            msg_message = btn_status, 
            msg_date = date_today, 
            msg_head_id = osas_r_auth_user.objects.get(auth_id = osas_id), 
            msg_send_to = s.org_abbr, 
            msg_send_from = osas_id)
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def concept_paper_osas_msg(request):
    class_id = request.POST.get('class_id')
    osas_id = request.POST.get('osas_id')
    btn_status = request.POST.get('msg')
    date_today = request.POST.get('date_today')
    s = classroom.objects.get(room_id = class_id)
    course_name = s.room_stud_id.stud_course_id.course_name
    class_year = s.room_year
    class_sec = s.room_sec
    class_name = course_name + ' ' + class_year
    try:
        today = datetime.today()
        d = organization_chat(
            msg_message = btn_status, 
            msg_date = date_today, 
            msg_head_id = osas_r_auth_user.objects.get(auth_id = osas_id), 
            msg_send_to = class_name, 
            msg_send_from = osas_id)
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}   
        return JsonResponse(data, safe=False)

def concept_paper_class_msg(request):
    class_id = request.POST.get('class_id')
    osas_id = request.POST.get('osas_id')
    osas_role_ = request.POST.get('osas_role_')
    btn_status = request.POST.get('msg')
    date_today = request.POST.get('date_today')
    s = classroom.objects.get(room_id = class_id)
    course_name = s.room_stud_id.stud_course_id.course_name
    class_year = s.room_year
    class_sec = s.room_sec
    class_name = course_name + ' ' + class_year
    try:
        today = datetime.today()
        d = organization_chat(
            msg_message = btn_status, 
            msg_date = date_today, 
            msg_room_id = classroom.objects.get(room_id = class_id),
            msg_head_id = osas_r_auth_user.objects.get(auth_id = osas_id), 
            msg_send_to = osas_role_, 
            msg_send_from = class_name)
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def accreditation_org_msg(request):
    org_id = request.POST.get('org_id')
    osas_id = request.POST.get('osas_id')
    btn_status = request.POST.get('msg')
    date_today = request.POST.get('date_today')
    try:
        today = datetime.today()
        role = osas_r_auth_user.objects.get(auth_id = osas_id),
        org = organization.objects.get(org_id = org_id)
        d = organization_chat(
            msg_message = btn_status, 
            msg_date = date_today, 
            msg_org_id = organization.objects.get(org_id = org_id), 
            msg_send_to = osas_id,
            msg_send_from = org.org_abbr)
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def conceptpaper_upload(request):
    docu = request.FILES.get('file')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    if request.method == 'POST':
        p = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id'])).count()
        if p < 8:
            org_concept_paper.objects.create(con_file = docu, con_org_id = organization.objects.get(org_id = request.session['session_user_id']), con_file_ext = extension)
            return HttpResponse('')
    return JsonResponse({'error': True})

def classroom_conceptpaper_upload(request):
    docu = request.FILES.get('file')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    if request.method == 'POST':
        p = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id'])).count()
        if p < 8:
            org_concept_paper.objects.create(con_file = docu, con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_file_ext = extension)
            return HttpResponse('')
    return JsonResponse({'error': True})

def classroom_concept_paper_upload(request):
    docu = request.FILES.get('file')
    room_id2 = request.POST.get('room_id2')
    title_id2 = request.POST.get('title_id2')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    if request.method == 'POST':
        p = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id'])).count()
        org_concept_paper.objects.create(con_file = docu, con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_file_ext = extension, con_status = 'SENT', con_title_id = concept_paper_title.objects.get(title_id = title_id2))
        return HttpResponse('')


def classroom_accomplishment_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    title_id2 = request.POST.get('title_id2')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    today = datetime.today()
    if request.method == 'POST':
        try:
            a = concept_paper_title.objects.get(title_id = title_id2, title_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
            a.title_accomplishment_file = docu
            a.title_accomplishment_file_ext = extension
            a.title_date_accomplished = today
            a.title_status = 'ACCOMPLISHED'
            a.save()
            return HttpResponse('')
        except ObjectDoesNotExist:
            return HttpResponse('')
    return JsonResponse({'error': True})

def organization_concept_paper_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    title_id2 = request.POST.get('title_id2')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    if request.method == 'POST':
        p = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id'])).count()
        org_concept_paper.objects.create(con_file = docu, con_org_id = organization.objects.get(org_id = request.session['session_user_id']), con_file_ext = extension, con_status = 'SENT', con_title_id = concept_paper_title.objects.get(title_id = title_id2))
        return HttpResponse('')

def organization_accomplishment_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    title_id2 = request.POST.get('title_id2')
    filename = str(docu)
    extension = filename.split(".")[1]
    print (extension)
    today = datetime.today()
    if request.method == 'POST':
        try:
            a = concept_paper_title.objects.get(title_id = title_id2, title_org_id = organization.objects.get(org_id = request.session['session_user_id']))
            a.title_accomplishment_file = docu
            a.title_accomplishment_file_ext = extension
            a.title_date_accomplished = today
            a.title_status = 'ACCOMPLISHED'
            a.save()
            return HttpResponse('')
        except ObjectDoesNotExist:
            return HttpResponse('')
    return JsonResponse({'error': True})


def organization_concept_papers(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    d = organization.objects.filter(org_id = request.session['session_user_id'])
    if acad_year and status:
        files = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id']), con_status = status, con_datecreated__contains = year ).order_by('-con_datecreated')
        return render(request, 'Organization/concept_papers.html', {'files':files, 'd':d})
    elif status:
        files = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id']), con_status = status).order_by('-con_datecreated')
        return render(request, 'Organization/concept_papers.html', {'files':files, 'd':d})
    elif acad_year:
        files = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id']), con_datecreated__contains = year ).order_by('-con_datecreated')
        return render(request, 'Organization/concept_papers.html', {'files':files, 'd':d})
    else:
        files = org_concept_paper.objects.filter(con_org_id = organization.objects.get(org_id = request.session['session_user_id']),con_status = "SAVED").order_by('-con_datecreated')
        return render(request, 'Organization/concept_papers.html', {'files':files, 'd':d})
    
def class_concept_papers(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    d = classroom.objects.filter(room_id = request.session['session_user_id'])
    if acad_year and status:
        files = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_status = status, con_datecreated__contains = year ).order_by('-con_datecreated')
        return render(request, 'classroom/concept_paper.html', {'files':files, 'd':d})
    elif status:
        files = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_status = status).order_by('-con_datecreated')
        return render(request, 'classroom/concept_paper.html', {'files':files, 'd':d})
    elif acad_year:
        files = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_datecreated__contains = year ).order_by('-con_datecreated')
        return render(request, 'classroom/concept_paper.html', {'files':files, 'd':d})
    else:
        files = org_concept_paper.objects.filter(con_room_id = classroom.objects.get(room_id = request.session['session_user_id']),con_status = "SAVED").order_by('-con_datecreated')
        return render(request, 'classroom/concept_paper.html', {'files':files, 'd':d})


def concept_papers(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    acc_docu_list = org_concept_paper.objects.all().filter(con_status = 'SENT')

    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        file_list = concept_paper_title.objects.all().filter(title_status = status, title_datecreated__contains = year).order_by("-title_datecreated")
        acc_list = organization.objects.all().filter(org_status = status, org_date_accredited__contains = year).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    elif acad_year:
        file_list = concept_paper_title.objects.all().filter(title_datecreated__contains = year).order_by("-title_datecreated")
        acc_list = organization.objects.all().filter(org_date_accredited__contains = year).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    if status:
        file_list = concept_paper_title.objects.all().filter(title_status = status).order_by("-title_datecreated")
        acc_list = organization.objects.all().filter(org_status = status ).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    else:
        file_list = concept_paper_title.objects.all().order_by("-title_datecreated")
        acc_list = organization.objects.all().order_by("-org_date_accredited")   
        class_list = classroom.objects.all().order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})

def concept_document_remove(request):
    doc_id = request.POST.get('con_id_')
    try:
        d = org_concept_paper.objects.get(con_id = doc_id)
        d.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def classroom_event_remove(request):
    title_id = request.POST.get('title_id')
    try:
        c = concept_paper_title.objects.get(title_id = title_id)
        d_list = org_concept_paper.objects.filter(con_title_id = concept_paper_title.objects.get(title_id = title_id))
        for x in d_list:
            x.delete()
        c.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def organization_inbox(request): 
    return render(request, 'Organization/inbox.html')

def student_events(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    acc_docu_list = org_concept_paper.objects.all().filter(con_status = 'SENT')
    
    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        file_list_room = concept_paper_title.objects.all().filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id']), title_status = status, title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    elif acad_year:
        file_list_room = concept_paper_title.objects.all().filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id']), title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', { 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    if status:
        file_list_room = concept_paper_title.objects.all().filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id']), title_status = status).order_by("-title_datecreated")
        file_list = concept_paper_title.objects.all().filter(title_status = status).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    else:
        file_list_room = concept_paper_title.objects.all().filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id'])).order_by("-title_datecreated")
        class_list = classroom.objects.all().order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})

def organization_events(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    acc_docu_list = org_concept_paper.objects.all().filter(con_status = 'SENT')
    
    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        file_list_org = concept_paper_title.objects.all().filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id']), title_status = status, title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    elif acad_year:
        file_list_org = concept_paper_title.objects.all().filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id']),  title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', { 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    if status:
        file_list_org = concept_paper_title.objects.all().filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id']), title_status = status).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    else:
        file_list_org = concept_paper_title.objects.all().filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id'])).order_by("-title_datecreated")
        class_list = classroom.objects.all().order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})

def classroom_event_populate(request):
    room_id = request.POST.get('room_id')
    title_id = request.POST.get('title_id')
    title_name = request.POST.get('title_name')
    doc_list = list(org_concept_paper.objects.filter(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_room_id = classroom.objects.get(room_id = room_id)).values())
    room_id = classroom.objects.get(room_id = room_id)
    return JsonResponse({
        'data': doc_list,
        'room_id':room_id.room_id
    })

def organization_event_populate(request):
    org_id = request.POST.get('org_id')
    title_id = request.POST.get('title_id')
    title_name = request.POST.get('title_name')
    doc_list = list(org_concept_paper.objects.filter(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_org_id = organization.objects.get(org_id = org_id)).values())
    org_id = organization.objects.get(org_id = org_id)
    return JsonResponse({
        'data': doc_list,
        'org_id':org_id.org_id
    })

def classroom_event_change_title(request):
    title_id = request.POST.get('title_id')
    title_name = request.POST.get('title_name')
    try:
        concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        d = concept_paper_title.objects.get(title_id = title_id)
        d.title_name = title_name
        d.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)

def gen_report_get_info_classroom(request):
    model_id = request.POST.get('model_id')
    mode = request.POST.get('type')
    try:
        if mode == 'classroom':
            c = classroom.objects.get(room_id = model_id)
            data = {'success':c.room_stud_id.stud_course_id.course_name + ' ' + c.room_year}
        if mode == 'organization':
            c = organization.objects.get(org_id = model_id)
            data = {'success':c.org_name}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
        
def gen_report_get_info_organization(request):
    org_id = request.POST.get('org_id')
    try:
        c = organization.objects.get(org_id = org_id)
        data = {'success':c.org_name}
        print(data)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
        
def orgnaization_request_fund(request):
    fund_desc = request.POST.get('fund_desc')
    fund_amount = request.POST.get('fund_amount')
    word = request.POST.get('fund_word')
    fund_word = word + ' Pesos Only'
    org_id = request.POST.get('org_id')
    type_fund = request.POST.get('type_fund')
    print(type_fund)
    status = request.POST.get('foredit')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    serial_no = 'SN-' + randomstr
    if type_fund == 'DEPOSIT':
        if status:
            fund_id = request.POST.get('fund_id')
            f = fund.objects.get(fund_id = fund_id,fund_org_id = organization.objects.get(org_id = org_id))
            f.fund_desc = fund_desc
            f.fund_amount = fund_amount
            f.fund_word = fund_word
            f.fund_type = type_fund
            f.save()
        else:
            fund.objects.create(fund_serial = serial_no,fund_desc = fund_desc, fund_amount = fund_amount, fund_word = fund_word, fund_org_id = organization.objects.get(org_id = org_id), fund_type = 'DEPOSIT')
        data = {'success':True}
        return JsonResponse(data, safe=False)
    elif type_fund == 'REQUEST':
        b = organization.objects.get(org_id = org_id)

        if b.org_fund > int(fund_amount):
            if status:
                fund_id = request.POST.get('fund_id')
                f = fund.objects.get(fund_id = fund_id,fund_org_id = organization.objects.get(org_id = org_id))
                f.fund_desc = fund_desc
                f.fund_amount = fund_amount
                f.fund_word = fund_word
                f.fund_type = type_fund
                f.save()
            else:
                fund.objects.create(fund_serial = serial_no, fund_desc = fund_desc, fund_amount = fund_amount, fund_word = fund_word, fund_org_id = organization.objects.get(org_id = org_id), fund_type = 'REQUEST')
            data = {'success':True}
            return JsonResponse(data, safe=False)
        else:
            print('hahaha')
            data = {'error':True}
            return JsonResponse(data, safe=False)

def osas_fund(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    fund_type = request.POST.get('fund_type')
    year = str(acad_year)
    file_list = fund_file.objects.all()
    fund_pending = fund.objects.filter(fund_status = 'PENDING', fund_type = 'REQUEST')
    fund_deposit = fund.objects.filter(fund_status = 'PENDING', fund_type = 'DEPOSIT')
    fund_balance_negative = fund.objects.filter(fund_status = 'APPROVED', fund_type = 'REQUEST')
    fund_balance_positive = fund.objects.filter(fund_status = 'APPROVED', fund_type = 'DEPOSIT')
    i = 0
    j = 0
    k = 0
    l = 0
    for x in fund_balance_positive:
        k = k + x.fund_amount
    for l in fund_balance_negative:
        l = l + x.fund_amount

    for x in fund_pending:
        i = i + x.fund_amount
    for x in fund_deposit:
        j = j + x.fund_amount

    if acad_year and status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_date_requested__contains = year, fund_status = status, fund_type = fund_type)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif acad_year and status:
        fund_org_list = fund.objects.all().filter(fund_date_requested__contains = year, fund_status = status)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif acad_year and fund_type:
        fund_org_list = fund.objects.all().filter(fund_date_requested__contains = year, fund_type = fund_type)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_status = status, fund_type = fund_type)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif status:
        fund_org_list = fund.objects.all().filter(fund_status = status)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif acad_year:
        fund_org_list = fund.objects.all().filter(fund_date_requested__contains = year)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    elif fund_type:
        fund_org_list = fund.objects.all().filter(fund_type = fund_type)
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})
    else:
        fund_org_list = fund.objects.all()
        return render(request, 'Facilitation/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j})

def osas_fund_authentication(request):
    auth_pass = request.POST.get('auth_pass')
    trans_fund_id = request.POST.get('trans_fund_id')
    trans_fund_cat = request.POST.get('trans_fund_cat')
    trans_fund_type = request.POST.get('trans_fund_type')
    trans_fund_amount = request.POST.get('trans_fund_amount')
    trans_type = request.POST.get('trans_type')
    try:
        a = osas_r_auth_user.objects.get(auth_id = request.session['session_user_id'], auth_password = auth_pass)
        if trans_fund_type == 'class':
            try:
                o = fund.objects.get(fund_id = trans_fund_id, fund_room_id = classroom.objects.get(room_id = trans_fund_cat ))
                if trans_type == 'REQUEST':
                    c = classroom.objects.get(room_id = trans_fund_cat)
                    balance = c.room_fund
                    c.room_fund = balance - int(trans_fund_amount)
                    c.save()
                    o.fund_status = 'COMPLETED'
                    o.save()
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                elif trans_type == 'DEPOSIT':
                    c = classroom.objects.get(room_id = trans_fund_cat)
                    balance = c.room_fund
                    c.room_fund = balance + int(trans_fund_amount)
                    c.save()
                    o.fund_status = 'COMPLETED'
                    o.save()
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                else:
                    data = {'error1':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                data = {'error':True}
                return JsonResponse(data, safe=False)
        else:
            try:
                o = fund.objects.get(fund_id = trans_fund_id, fund_org_id = organization.objects.get(org_id = trans_fund_cat ))
                if trans_type == 'REQUEST':
                    c = organization.objects.get(org_id = trans_fund_cat)
                    balance = c.org_fund
                    c.org_fund = balance - int(trans_fund_amount)
                    c.save()
                    o.fund_status = 'COMPLETED'
                    o.save()
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                elif trans_type == 'DEPOSIT':
                    c = organization.objects.get(org_id = trans_fund_cat)
                    balance = c.org_fund
                    c.org_fund = balance + int(trans_fund_amount)
                    c.save()
                    o.fund_status = 'COMPLETED'
                    o.save()
                    data = {'success':True}
                    return JsonResponse(data, safe=False)
                else:
                    data = {'error1':True}
                    return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                data = {'error':True}
                return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)


def organization_fund(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    fund_type = request.POST.get('fund_type')
    year = str(acad_year)
    file_list = fund_file.objects.all().filter(fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']) )
    fund_pending = fund.objects.filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = 'PENDING', fund_type = 'REQUEST')
    fund_deposit = fund.objects.filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = 'PENDING', fund_type = 'DEPOSIT')
    fund_balance_negative = fund.objects.filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = 'APPROVED', fund_type = 'REQUEST')
    fund_balance_positive = fund.objects.filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = 'APPROVED', fund_type = 'DEPOSIT')
    i = 0
    j = 0
    k = 0
    l = 0
    for x in fund_balance_positive:
        k = k + x.fund_amount
    for l in fund_balance_negative:
        l = l + x.fund_amount

    for x in fund_pending:
        i = i + x.fund_amount
    for x in fund_deposit:
        j = j + x.fund_amount

    balance = k - l
    org_fund = organization.objects.get(org_id = request.session['session_user_id'])
    tot_bal = org_fund.org_fund
    print(tot_bal)
    if acad_year and status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_status = status, fund_type = fund_type)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year and status:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_status = status)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year and fund_type:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_type = fund_type)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = status, fund_type = fund_type)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif status:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = status)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif fund_type:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_type = fund_type)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    else:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']))
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})

def organization_deposit_fund(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    file_list = fund_file.objects.all().filter(fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']) )
    fund_pending = fund.objects.filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = 'APPROVED')
    i = 0
    for x in fund_pending:
        i = i + x.fund_amount
    print(i)
    if acad_year and status:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_status = status)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i})
    elif acad_year:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_date_requested__contains = year)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i})
    if status:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_status = status)
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i})
    else:
        fund_org_list = fund.objects.all().filter(fund_org_id = organization.objects.get(org_id = request.session['session_user_id']))
        return render(request, 'Organization/fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i})

def organization_fund_reciept_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    fund_id = request.POST.get('fund_id2')
    receipt = request.POST.get('receipt')
    fund_f_id = request.POST.get('fund_f_id')
    filename = str(docu)
    extension = filename.split(".")[1]
    try:
        if fund_f_id:
            f = fund_file.objects.get(fund_f_id = fund_f_id, fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']),  fund_f_status =  receipt)
            f.delete()
            fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
            return HttpResponse('')
        else:
            fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
            return HttpResponse('')
    except ObjectDoesNotExist:
        fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
        return HttpResponse('')
    
#create function for uploading logo
def organization_upload_logo(request):
    docu = request.FILES.get('file')
    try:
        o = organization.objects.get(org_id = request.session['session_user_id'])
        o.org_logo = docu
        o.save()
        return HttpResponse('')
    except ObjectDoesNotExist:
        return HttpResponse('')

def class_fund_reciept_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    fund_id = request.POST.get('fund_id2')
    receipt = request.POST.get('receipt')
    fund_f_id = request.POST.get('fund_f_id')
    filename = str(docu)
    extension = filename.split(".")[1]
    try:
        if fund_f_id:
            f = fund_file.objects.get(fund_f_id = fund_f_id, fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']),  fund_f_status =  receipt)
            f.delete()
            fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id),  fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
            return HttpResponse('')
        else:
            fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id),  fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
            return HttpResponse('')
    except ObjectDoesNotExist:
        fund_file.objects.create(fund_fund_id = fund.objects.get(fund_id = fund_id),  fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_f_file = docu, fund_f_file_ext = extension, fund_f_status =  receipt)
        return HttpResponse('')

def class_fund_populate(request):
    room_id = request.POST.get('room_id')
    fund_id = request.POST.get('fund_id')
    fund_list = list(fund.objects.filter(fund_id = fund_id, fund_room_id = classroom.objects.get(room_id = room_id)).values())
    room_id = classroom.objects.get(room_id = room_id)
    return JsonResponse({
        'data': fund_list,
        'org_id':room_id.room_id
    })

def organization_fund_populate(request):
    org_id = request.POST.get('org_id')
    fund_id = request.POST.get('fund_id')
    fund_list = list(fund.objects.filter(fund_id = fund_id, fund_org_id = organization.objects.get(org_id = org_id)).values())
    org_id = organization.objects.get(org_id = org_id)
    return JsonResponse({
        'data': fund_list,
        'org_id':org_id.org_id
    })


def fund_request_remove(request):
    fund_id = request.POST.get('fund_id')
    try:
        c = fund.objects.get(fund_id = fund_id)
        f_list = fund_file.objects.filter(fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_org_id = organization.objects.get(org_id = request.session['session_user_id']))
        for x in f_list:
            x.delete()
        c.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def classroom_fund_request_remove(request):
    fund_id = request.POST.get('fund_id')
    try:
        c = fund.objects.get(fund_id = fund_id)
        f_list = fund_file.objects.filter(fund_fund_id = fund.objects.get(fund_id = fund_id), fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
        for x in f_list:
            x.delete()
        c.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def classroom_fund(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    fund_type = request.POST.get('fund_type')
    year = str(acad_year)
    file_list = fund_file.objects.all().filter(fund_f_room_id = classroom.objects.get(room_id = request.session['session_user_id']) )
    fund_pending = fund.objects.filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = 'PENDING', fund_type = 'REQUEST')
    fund_deposit = fund.objects.filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = 'PENDING', fund_type = 'DEPOSIT')
    fund_balance_negative = fund.objects.filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = 'APPROVED', fund_type = 'REQUEST')
    fund_balance_positive = fund.objects.filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = 'APPROVED', fund_type = 'DEPOSIT')
    i = 0
    j = 0
    k = 0
    l = 0
    for x in fund_balance_positive:
        k = k + x.fund_amount
    for l in fund_balance_negative:
        l = l + x.fund_amount

    for x in fund_pending:
        i = i + x.fund_amount
    for x in fund_deposit:
        j = j + x.fund_amount

    balance = k - l
    class_fund = classroom.objects.get(room_id = request.session['session_user_id'])
    tot_bal = class_fund.room_fund
    print(tot_bal)

    if acad_year and status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_status = status, fund_type = fund_type)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year and status:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_status = status)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year and fund_type:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_date_requested__contains = year, fund_type = fund_type)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif status and fund_type:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = status, fund_type = fund_type)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif status:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_status = status)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif acad_year:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_date_requested__contains = year)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    elif fund_type:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']), fund_type = fund_type)
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})
    else:
        fund_org_list = fund.objects.all().filter(fund_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
        return render(request, 'classroom/class_fund.html', {'fund_org_list':fund_org_list, 'file_list':file_list, 'i':i,'j':j, 'balance':balance, 'tot_bal':tot_bal})

def class_request_fund(request):
    fund_desc = request.POST.get('fund_desc')
    fund_amount = request.POST.get('fund_amount')
    word = request.POST.get('fund_word')
    fund_word = word + ' Pesos Only'
    room_id = request.POST.get('room_id')
    type_fund = request.POST.get('type_fund')
    print(type_fund)
    status = request.POST.get('foredit')
    fund_id = request.POST.get('fund_id')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    serial_no = 'SN-' + randomstr
    if type_fund == 'DEPOSIT':
        if status:
            f = fund.objects.get(fund_id = fund_id,fund_room_id = classroom.objects.get(room_id = room_id))
            f.fund_desc = fund_desc
            f.fund_amount = fund_amount
            f.fund_word = fund_word
            f.fund_type = type_fund
            f.save()
        else:
            fund.objects.create(fund_serial = serial_no, fund_desc = fund_desc, fund_amount = fund_amount, fund_word = fund_word, fund_room_id = classroom.objects.get(room_id = room_id), fund_type = 'DEPOSIT')
        data = {'success':True}
        return JsonResponse(data, safe=False)
    elif type_fund == 'REQUEST':
        b = classroom.objects.get(room_id = room_id)
        f = fund.objects.filter(fund_room_id = classroom.objects.get(room_id = room_id), fund_status = 'PENDING', fund_type = 'REQUEST')
        i = 0
        for x in f:
            i = i + x.fund_amount
        tot_request = i + int(fund_amount)
        if b.room_fund >= tot_request :
            if status:
                fund_id = request.POST.get('fund_id')
                f = fund.objects.get(fund_id = fund_id,fund_room_id = classroom.objects.get(room_id = room_id))
                f.fund_desc = fund_desc
                f.fund_amount = fund_amount
                f.fund_word = fund_word
                f.fund_type = type_fund
                f.save()
            else:
                fund.objects.create(fund_serial = serial_no, fund_desc = fund_desc, fund_amount = fund_amount, fund_word = fund_word, fund_room_id = classroom.objects.get(room_id = room_id), fund_type = 'REQUEST')
            data = {'success':True}
            return JsonResponse(data, safe=False)
        else:
            data = {'error':True}
            return JsonResponse(data, safe=False)

def organization_officer(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    try:
        o = organization.objects.get(org_id = request.session['session_user_id'])
        if o.org_course == 'N/A':
            stud_list2 = osas_r_personal_info.objects.all()
        else:
            course = o.org_stud_id.stud_course_id.course_name
            stud_list2 = osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get(course_name = course))
        if acad_year and status:
            officer_list = officer.objects.all().filter(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_date_added__contains = year, off_status = status)
            return render(request, 'Organization/officers.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        elif acad_year:
            officer_list = officer.objects.all().filter(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_date_added__contains = year)
            return render(request, 'Organization/officers.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        if status:
            officer_list = officer.objects.all().filter(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_status = status)
            return render(request, 'Organization/officers.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        else:
            officer_list = officer.objects.all().filter(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_status = 'ACTIVE')
            return render(request, 'Organization/officers.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
    except ObjectDoesNotExist:
        print('error')

def classroom_officer(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    try:
        o = classroom.objects.get(room_id = request.session['session_user_id'])
        course = o.room_stud_id.stud_course_id.course_name
        stud_list2 = osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get(course_name = course))
        if acad_year and status:
            officer_list = officer.objects.all().filter(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_date_added__contains = year, off_status = status)
            return render(request, 'classroom/officer.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        elif acad_year:
            officer_list = officer.objects.all().filter(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_date_added__contains = year)
            return render(request, 'classroom/officer.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        if status:
            officer_list = officer.objects.all().filter(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_status = status)
            return render(request, 'classroom/officer.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
        else:
            officer_list = officer.objects.all().filter(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_status = 'ACTIVE')
            return render(request, 'classroom/officer.html', {'officer_list':officer_list, 'stud_list2':stud_list2})
    except ObjectDoesNotExist:
        print('error')

def classroom_add_officer(request):
    position = request.POST.get('position')
    stud_no = request.POST.get('stud_no')
    status = request.POST.get('foredit')
    if status:
        off_id = request.POST.get('off_id')
        room_id = request.POST.get('org_id')
        try:
            f = officer.objects.get(off_room_id = classroom.objects.get(room_id = room_id), off_position = position)
            if f:
                data = {'error':True}
                return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            f = officer.objects.get(off_id = off_id, off_room_id = classroom.objects.get(room_id = room_id))
            f.off_position = position
            f.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    else:
        try:
            f = officer.objects.get(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_position = position)
            data = {'error1':True}
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            try:
                o = officer.objects.get(off_room_id = classroom.objects.get(room_id = request.session['session_user_id']), off_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no))
                data = {'error':True}
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                officer.objects.create(off_position = position, off_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), off_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
    data = {'success':True}
    return JsonResponse(data, safe=False)

def orgnaization_add_officer(request):
    position = request.POST.get('position')
    stud_no = request.POST.get('stud_no')
    status = request.POST.get('foredit')
    if status:
        off_id = request.POST.get('off_id')
        org_id = request.POST.get('org_id')
        try:
            f = officer.objects.get(off_org_id = organization.objects.get(org_id = org_id), off_position = position)
            if f:
                data = {'error':True}
                return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            f = officer.objects.get(off_id = off_id, off_org_id = organization.objects.get(org_id = org_id))
            f.off_position = position
            f.save()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    else:
        try:
            f = officer.objects.get(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_position = position)
            data = {'error1':True}
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            try:
                o = officer.objects.get(off_org_id = organization.objects.get(org_id = request.session['session_user_id']), off_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no))
                data = {'error':True}
                return JsonResponse(data, safe=False)
            except ObjectDoesNotExist:
                officer.objects.create(off_position = position, off_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), off_org_id = organization.objects.get(org_id = request.session['session_user_id']))
    data = {'success':True}
    return JsonResponse(data, safe=False)

def organization_fund_voucher_gen(request):
    org_id = request.POST.get('org_id')
    fund_id = request.POST.get('fund_id')
    fund_list = list(fund.objects.filter(fund_id = fund_id, fund_org_id = organization.objects.get(org_id = org_id)).values())
    off_list = list(officer.objects.all().filter(off_org_id = organization.objects.get(org_id = org_id)).values())
    org_id = organization.objects.get(org_id = org_id)
    return JsonResponse({
        'data': fund_list,
        'data2':off_list,
        'org_id':org_id.org_id
    })

def class_fund_voucher_gen(request):
    room_id = request.POST.get('room_id')
    fund_id = request.POST.get('fund_id')
    fund_list = list(fund.objects.filter(fund_id = fund_id, fund_room_id = classroom.objects.get(room_id = room_id)).values())
    off_list = list(officer.objects.all().filter(off_room_id = classroom.objects.get(room_id = room_id)).values())
    room_id = classroom.objects.get(room_id = room_id)
    return JsonResponse({
        'data': fund_list,
        'data2':off_list,
        'org_id':room_id.room_id
    })
def organization_signature_upload(request):
    docu = request.FILES.get('file')
    org_id2 = request.POST.get('org_id2')
    off_id = request.POST.get('officer_id2')
    filename = str(docu)
    extension = filename.split(".")[1]
    try:
        f = officer.objects.get(off_id = off_id, off_org_id = organization.objects.get(org_id = request.session['session_user_id']))
        if f.off_signature == None:
            f.off_signature = docu
            f.off_signature_ext = extension
            f.save()
        else:
            off_position = f.off_position
            off_stud_id = f.off_stud_id.stud_id
            off_status = f.off_status
            f.delete()
            officer.objects.create(off_position = off_position, off_stud_id = osas_r_personal_info.objects.get(stud_id = off_stud_id), off_status = off_status, off_org_id =  organization.objects.get(org_id = request.session['session_user_id']), off_signature = docu, off_signature_ext = extension )
        return HttpResponse('')
    except ObjectDoesNotExist:
        return HttpResponse('')
        
def officer_remove(request):
    off_id = request.POST.get('off_id')
    org_id = request.POST.get('org_id')
    cat = request.POST.get('category_')
    try:
        if cat:
            c = officer.objects.get(off_id = off_id, off_room_id = classroom.objects.get(room_id = org_id))
            c.delete()
            data = {'success':True}
            return JsonResponse(data, safe=False)
        else:
            c = officer.objects.get(off_id = off_id, off_org_id = organization.objects.get(org_id = org_id))
            c.delete()
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)