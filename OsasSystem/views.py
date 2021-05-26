import random
import os.path
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import osas_r_userrole, osas_r_course, osas_r_section_and_year, osas_r_personal_info, osas_r_auth_user, osas_t_id, osas_t_sanction, osas_r_code_title, osas_r_disciplinary_sanction, osas_r_designation_office, osas_t_excuse, osas_t_complaint, osas_notif, organization, org_accreditation, organization_chat, org_concept_paper,classroom, concept_paper_title
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



def notif_seen(request):
    notif_lost_id = request.POST.get('notif_lost_id')
    notif = osas_notif.objects.get(notif_lost_id = notif_lost_id)
    notif.notif_head = "Seen"
    notif.save()
    data = {'success':notif_lost_id}
    return JsonResponse(data, safe=False)

def notif_sanction(request):
    sanction_id = request.POST.get('sanction_id')
    notif = osas_notif.objects.get(notif_sanction_id = sanction_id)
    notif.notif_head = "Seen"
    notif.save()
    data = {'success':sanction_id}
    return JsonResponse(data, safe=False)

def notif_seen_stud(request):
    notif_lost_id = request.POST.get('notif_lost_id')
    notif = osas_notif.objects.get(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_lost_id = notif_lost_id)
    notif.notif_stud = "Seen"
    notif.save()
    data = {'success':notif_lost_id}
    return JsonResponse(data, safe=False)

def notif_sanction_stud(request):
    sanction_id = request.POST.get('sanction_id')
    notif = osas_notif.objects.get(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_sanction_id = sanction_id)
    notif.notif_stud = "Seen"
    notif.save()
    data = {'success':sanction_id}
    return JsonResponse(data, safe=False)

def home(request):
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")

    stud_bbtled =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BBTLEDHE')).count()
    stud_bsit =  osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSIT')).count()
    stud_bsbamm =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBA-MM')).count()
    stud_bsbahrm = osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSBAHRM')).count()
    stud_bsent =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'BSENTREP')).count()
    stud_domt =  osas_r_personal_info.objects.filter(stud_course_id = osas_r_course.objects.get( course_code = 'DOMTMOM')).count()

    student_count = osas_r_personal_info.objects.all().count()
    lost_id_count = osas_t_id.objects.all().count()
    sanction_count = osas_t_sanction.objects.all().count()
    grievances_count = osas_t_complaint.objects.all().count()

    lost_id_pending = osas_t_id.objects.filter(lost_id_status__iexact = 'PENDING').count()
    lost_id_process = osas_t_id.objects.filter(lost_id_status__iexact = 'PROCESSING').count()
    lost_id_completed = osas_t_id.objects.filter(lost_id_status__iexact = 'COMPLETED').count()

    complaint_pending = osas_t_complaint.objects.filter(comp_status__iexact = 'PENDING').count()
    complaint_approved = osas_t_complaint.objects.filter(comp_status__iexact = 'APPROVED').count()
    complaint_decline = osas_t_complaint.objects.filter(comp_status__iexact = 'DECLINED').count()

    sanction_pending = osas_t_sanction.objects.filter(sanction_status__iexact = 'PENDING').count()
    sanction_active = osas_t_sanction.objects.filter(sanction_status__iexact = 'ACTIVE').count()
    sanction_completed = osas_t_sanction.objects.filter(sanction_status__iexact = 'COMPLETED').count()
    sanction_excused = osas_t_sanction.objects.filter(sanction_status__iexact = 'EXCUSED').count()
    
    return render(request, 'home.html', {'stud_bbtled':stud_bbtled, 'stud_bsit':stud_bsit, 'stud_bsbamm':stud_bsbamm, 'stud_bsbahrm':stud_bsbahrm, 'stud_bsent':stud_bsent, 'stud_domt':stud_domt, 'lost_id_pending':lost_id_pending, 'lost_id_process':lost_id_process, 'lost_id_completed':lost_id_completed, 'sanction_pending':sanction_pending, 'sanction_active':sanction_active, 'sanction_completed':sanction_completed, 'sanction_excused':sanction_excused, 'complaint_pending':complaint_pending, 'complaint_approved':complaint_approved, 'complaint_decline':complaint_decline, 'student_count':student_count, 'lost_id_count':lost_id_count, 'sanction_count':sanction_count, 'grievances_count':grievances_count, 'notif':notif, 'notif_info':notif_info})

def dashboard(request):
    notif = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = "Sent").order_by("-notif_datecreated")
    lost_id_pending = osas_t_id.objects.filter(lost_stud_id = request.session['session_user_id'], lost_id_status__iexact = 'PENDING').count()
    lost_id_process = osas_t_id.objects.filter(lost_stud_id = request.session['session_user_id'],lost_id_status__iexact = 'PROCESSING').count()
    lost_id_completed = osas_t_id.objects.filter(lost_stud_id = request.session['session_user_id'],lost_id_status__iexact = 'COMPLETED').count()

    complaint_pending = osas_t_complaint.objects.filter(comp_stud_id = request.session['session_user_id'], comp_status__iexact = 'PENDING').count()
    complaint_approved = osas_t_complaint.objects.filter(comp_stud_id = request.session['session_user_id'], comp_status__iexact = 'APPROVED').count()
    complaint_decline = osas_t_complaint.objects.filter(comp_stud_id = request.session['session_user_id'], comp_status__iexact = 'DECLINED').count()

    sanction_pending = osas_t_sanction.objects.filter(sanction_stud_id = request.session['session_user_id'], sanction_status__iexact = 'PENDING').count()
    sanction_active = osas_t_sanction.objects.filter(sanction_stud_id = request.session['session_user_id'], sanction_status__iexact = 'ACTIVE').count()
    sanction_completed = osas_t_sanction.objects.filter(sanction_stud_id = request.session['session_user_id'], sanction_status__iexact = 'COMPLETED').count()
    sanction_excused = osas_t_sanction.objects.filter(sanction_stud_id = request.session['session_user_id'], sanction_status__iexact = 'EXCUSED').count()

    return render(request, 'Role_Student/dashboard.html', {'lost_id_pending':lost_id_pending, 'lost_id_process':lost_id_process, 'lost_id_completed':lost_id_completed, 'sanction_pending':sanction_pending, 'sanction_active':sanction_active, 'sanction_completed':sanction_completed, 'sanction_excused':sanction_excused, 'complaint_pending':complaint_pending, 'complaint_approved':complaint_approved, 'complaint_decline':complaint_decline, 'notif':notif,'notif_info':notif_info})
#--------------------------------------LOGIN------------------------------------------------------------------------------------------
def welcome(request):
    return render(request, 'welcome.html')

def login(request):
    try:
        del request.session['session_user_role']
        request.session['session_user_role'] = 'none'
        return render(request, 'login.html', {})
    except KeyError:
        return render(request, 'login.html', {})

def logout(request):
    try:
        del request.session['session_user_role']
        request.session['session_user_role'] = 'none'
        return render(request, 'login.html', {})
    except KeyError:
        return render(request, 'login.html', {})

def activate_account(request):
    s_no = request.POST.get('stud_no')
    password = request.POST.get('pass')
    try:
        stud = osas_r_personal_info.objects.get(stud_no=s_no)
        c = osas_r_personal_info.objects.filter(stud_no=s_no, s_password= password )
        # s = osas_r_userrole.objects.get(user_id= stud.stud_role)
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
                return HttpResponseRedirect('/dashboard') #passing the values of student to the next template
        else:
            messages.error(request, 'Either student number or password are incorrect.')
            return HttpResponseRedirect('/login')
    except ObjectDoesNotExist:
        u = osas_r_auth_user.objects.filter(auth_username=s_no).count()
        c = organization.objects.filter(org_email=s_no)
        if u:
            r = osas_r_auth_user.objects.get(auth_username = s_no)
            # userrole = r.auth_id
            # f = osas_r_userrole.objects.get(user_id = userrole)
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
                    request.session['session_user_lname'] = room3.room_stud_id.stud_course_id.course_name + ' ' + room3.room_year + ' - ' + room3.room_sec
                    request.session['session_class_year'] = room3.room_year
                    request.session['session_class_section'] = room3.room_sec
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

def account_process(request):
    s_no = request.POST.get('r_studno')
    old_pass = request.POST.get('r_pass')
    new_pass = request.POST.get('r_pass1')
    conf_pass = request.POST.get('r_pass2')
    try:
        if s_no:
            stud = osas_r_personal_info.objects.get(stud_no=s_no)
            if stud.stud_no == s_no:
                if stud.s_password == old_pass:
                    if new_pass and conf_pass:
                        if new_pass == conf_pass:
                            stud.s_password = conf_pass
                            stud.stud_status = 'ACTIVE'
                            stud.save()
                            return HttpResponseRedirect('/login')
    
                        else:
                            messages.error(request, 'Password does not match, please try again.')
                            # return HttpResponseRedirect('/activate_account', {'stud': stud}) 
                            return render(request, 'activate_account.html')  
                    else:  
                        messages.error(request, 'Please enter your new and confirm password.')
                        return HttpResponseRedirect('/activate_account') 
                else:
                    messages.error(request, 'Please enter your correct old password.')
                    return HttpResponseRedirect('/activate_account') 
            else: 
                messages.error(request, 'Invalid student number' )
                return HttpResponseRedirect('/activate_account') 
        else:
            messages.error(request, 'Invalid student number' )
            return HttpResponseRedirect('/activate_account') 
    except ObjectDoesNotExist:
        messages.error(request, 'Invalid account!')
        return HttpResponseRedirect('/activate_account') 
    

def r_employ(request):
    return render(request, 'alumni/r_employ.html')
   
    
#------------------------------------YEAR AND SECTION------------------------------------------------------------------------------------
def yr_sec(request):
    status = request.POST.get('filter_status')
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if status:
            user_list = osas_r_section_and_year.objects.all().filter(status = status ).order_by('yas_descriptions')
            context = {'user_list': user_list}
            return render(request, 'year_section/yr_sec.html', {'user_list':user_list, 'notif':notif, 'notif_info':notif_info})
    else:   
        user_list = osas_r_section_and_year.objects.all().filter(status = "ACTIVE").order_by('yas_descriptions')
        context = {'user_list': user_list}
        return render(request, 'year_section/yr_sec.html', {'user_list':user_list, 'notif':notif, 'notif_info':notif_info})
    

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
                    # u.save()
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
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if filter_code and filter_name:
        if status:
            course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_name = filter_name, course_status = status ).order_by('course_code')
            return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
        else:   
            course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_name = filter_name).order_by('course_code')
            return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    elif filter_code and status:
        course_list = osas_r_course.objects.all().filter(course_code = filter_code, course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    elif filter_name and status:
        course_list = osas_r_course.objects.all().filter(course_name = filter_name, course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    elif status:
        course_list = osas_r_course.objects.all().filter(course_status = status ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    elif filter_name:
        course_list = osas_r_course.objects.all().filter(course_name = filter_name ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    elif filter_code:
        course_list = osas_r_course.objects.all().filter(course_code = filter_code ).order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})
    else:
        course_list = osas_r_course.objects.all().filter(course_status = "ACTIVE").order_by('course_code')
        return render(request, 'course/course.html', {'course_list':course_list, 'course_lists':course_lists, 'notif':notif, 'notif_info':notif_info})

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
                    # u.save()
                
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
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if txt_course1 and txt_yr_sec1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_course1 and txt_yr_sec1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_course1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_yr_sec1 and txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1), stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_course1:
        student_info = osas_r_personal_info.objects.all().filter(stud_course_id = osas_r_course.objects.get(course_name = txt_course1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_Gender1:
        student_info = osas_r_personal_info.objects.all().filter(stud_gender = txt_Gender1).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    elif txt_yr_sec1:
        student_info = osas_r_personal_info.objects.all().filter(stud_yas_id = osas_r_section_and_year.objects.get(yas_descriptions = txt_yr_sec1)).order_by('stud_no')
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})
    else:
        return render(request, template_name, {'student_info': student_info, 'student_course': student_course, 'student_yr_sec': student_yr_sec, 'notif':notif, 'notif_info':notif_info})

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
            stud_role = osas_r_userrole.objects.get(user_type='STUDENT'), 
            stud_course_id = osas_r_course.objects.get(course_name = course), 
            stud_yas_id  = osas_r_section_and_year.objects.get(yas_descriptions = yr_sec))
        stud.save()   
        data = {'success':True}
        return JsonResponse(data, safe=False)
        # return HttpResponseRedirect('/student_profile' , {'success_message': "Congratulations," + " " + studno + "is successfully register."})
       
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
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    return render(request, 'userrole.html', {'user_list': user_list,'notif':notif, 'notif_info':notif_info})
    
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
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if date1 and date2:
        if status:
            auth_user = osas_r_auth_user.objects.all().filter(auth_status = status, date_updated__range=[date1, date2], auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
            return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole, 'notif':notif, 'notif_info':notif_info})
        else:   
            auth_user = osas_r_auth_user.objects.all().filter(date_updated__range=[date1, date2], auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
            return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole, 'notif':notif, 'notif_info':notif_info})
    elif status:
        auth_user = osas_r_auth_user.objects.all().filter(auth_status = status, auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF")).order_by('-date_updated')
        return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole, 'notif':notif, 'notif_info':notif_info})
    else:
        auth_user = osas_r_auth_user.objects.all().filter(auth_role = osas_r_userrole.objects.get(user_type = "OSAS STAFF"), auth_status = "ACTIVE").order_by('-date_updated')
        return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole, 'notif':notif, 'notif_info':notif_info})
    

def auth_process_edit(request, auth_id):
    template_name = 'auth_process_edit.html'
    # auth = osas_r_auth_user.objects.order_by('auth_username')
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

#-------------------------------------STUDENT SIDE---------------------------------------------------------

def id_request_form(request):
    return render(request, 'Role_Student/id_request_form.html')

def student_lost_id(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    if status == "On Process":
        status = "PROCESSING"
    notif = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = "Sent").order_by("-notif_datecreated")
    if date1 and date2:
        if status:
            stud_info = osas_t_id.objects.all().filter(lost_stud_id = request.session['session_user_id'], lost_id_status = status, date_updated__range=[date1, date2]).order_by('-date_created')
            return render(request, 'Role_Student/student_lost_id.html', {'stud_info': stud_info, 'notif':notif, 'notif_info':notif_info})
        else:   
            stud_info = osas_t_id.objects.all().filter(lost_stud_id = request.session['session_user_id'], date_updated__range=[date1, date2]).order_by('-date_created')
            return render(request, 'Role_Student/student_lost_id.html', {'stud_info': stud_info, 'notif':notif, 'notif_info':notif_info})
    elif status:
        stud_info = osas_t_id.objects.all().filter(lost_stud_id = request.session['session_user_id'], lost_id_status = status).order_by('-date_created')
        return render(request, 'Role_Student/student_lost_id.html', {'stud_info': stud_info, 'notif':notif, 'notif_info':notif_info})
    else:
        stud_info = osas_t_id.objects.all().filter(lost_stud_id = request.session['session_user_id']).order_by('-date_created')
        return render(request, 'Role_Student/student_lost_id.html', {'stud_info': stud_info, 'notif':notif, 'notif_info':notif_info})

#-----------------------------ID---------------------------------------------------------------------------
def lost_id(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    if status == "On Process":
        status = "PROCESSING"
    id_request =  osas_t_id.objects.all().order_by('-date_created')
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    stud_list = osas_t_id.objects.filter(lost_id_status = 'COMPLETE') # queryset for all existing student_no
    stud_ = osas_r_personal_info.objects.all()
    stud_list2 = osas_r_personal_info.objects.filter(stud_id__in = stud_.values_list('stud_id',)) # queryset for all the student then exclude the data that existing in the osas_t_id
   
    if date1 and date2:
        if status:
            id_request = osas_t_id.objects.all().filter(lost_id_status = status, date_updated__range=[date1, date2]).order_by('-date_created')
            return render(request, 'id/lost_id.html', {'stud_list2': stud_list2, 'id_request': id_request, 'stud_list':stud_list, 'notif':notif, 'notif_info':notif_info})
        else:   
            id_request = osas_t_id.objects.all().filter(date_updated__range=[date1, date2]).order_by('-date_created')
            return render(request, 'id/lost_id.html', {'stud_list2': stud_list2, 'id_request': id_request, 'stud_list':stud_list, 'notif':notif, 'notif_info':notif_info})
    elif status:
        id_request = osas_t_id.objects.all().filter(lost_id_status = status).order_by('-date_created')
        return render(request, 'id/lost_id.html', {'stud_list2': stud_list2, 'id_request': id_request, 'stud_list':stud_list, 'notif':notif, 'notif_info':notif_info})
    else:
        id_request = osas_t_id.objects.all().order_by('-date_created')
        return render(request, 'id/lost_id.html', {'stud_list2': stud_list2, 'id_request': id_request, 'stud_list':stud_list, 'notif':notif, 'notif_info':notif_info})

def lost_id_student_data(request):
    selected_student = request.POST.get('selected_student')
    try:
        t = osas_r_personal_info.objects.get(stud_no = selected_student)
        id_count = osas_t_id.objects.all().filter(lost_stud_id = osas_r_personal_info.objects.get(stud_no = selected_student), lost_id_status = 'PENDING').count()
        data = {
            'lname': t.stud_lname,
            'fname': t.stud_fname,
            'mname': t.stud_mname,
            'sname': t.stud_sname,
            'course': t.stud_course_id.course_name,
            'count':id_count
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'id/lost_id.html')

def id_request_process(request): 
    r_id = request.POST.get('lost_id')
    status = request.POST.get('status')
    stud = request.POST.get('stud')
    notif = osas_notif.objects.get(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_lost_id = r_id)
    notif.notif_stud = "Sent"
    notif.save()
    try:
        today = datetime.today()
        if status == "PENDING":
            status = 'PROCESSING'
        elif status == "PROCESSING":
            status = 'COMPLETED'
        else:
            status = 'ARCHIVE'
        id_request = osas_t_id.objects.get(lost_id = r_id)
        id_request.lost_id_status = status
        id_request.date_updated = today
        id_request.save()   
      
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': id_request.lost_id_status}
        return JsonResponse(data, safe=False)

def id_request_completed(request):
    r_id = request.POST.get('request_id')
    try:
        today = datetime.today()
        id_request = osas_t_id.objects.get(request_id = r_id)
        id_request.lost_id_status = 'COMPLETED'
        id_request.date_updated = today
        id_request.save()   
        return HttpResponseRedirect('/lost_id')
    except ObjectDoesNotExist:
        return render(request, 'id/lost_id.html')

def id_request_remove(request):
    r_id = request.POST.get('lost_id')
    try:
        today = datetime.today()
        osas_t_sanction.objects.get(sanction_t_id = osas_t_id.objects.get(lost_id = r_id)).delete()
        s = osas_t_id.objects.get(lost_id = r_id).delete()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': r_id}
        return JsonResponse(data, safe=False)


def lost_id_view(request):
    today = datetime.today()
    lost_id_ = request.POST.get('lost_id')
    try:
        d = osas_t_id.objects.get(lost_id = lost_id_)
        count = osas_t_id.objects.filter(lost_stud_id = d.lost_stud_id).exclude(lost_id_status = "CANCELLED").count()

        lost_Id_val = {
            'id':d.lost_id,
            'r_id':d.request_id,
            'date':d.date_created,
            'status':d.lost_id_status,
            'stud_no':d.lost_stud_id.stud_no,
            'stud_lname':d.lost_stud_id.stud_lname,
            'stud_fname':d.lost_stud_id.stud_fname,
            'stud_mname':d.lost_stud_id.stud_mname,
            'course':d.lost_stud_id.stud_course_id.course_name,
            'year':d.lost_stud_id.stud_yas_id.yas_descriptions,
            'dob':d.lost_stud_id.stud_birthdate,
            'gender':d.lost_stud_id.stud_gender,
            'address':d.lost_stud_id.stud_address,
            'email':d.lost_stud_id.stud_email,
            'contact':d.lost_stud_id.stud_m_number,
            'count':count,
        }
        data = {'lost_Id_val':lost_Id_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:  
        data = {'error':True}
        return JsonResponse(data, safe=False)


def add_id_request(request):

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(8))
    r_id = randomstr
    no = request.POST.get('stud')
    stud = osas_r_personal_info.objects.get(stud_no = no)
    if stud:
        if not no == '--select--':
            n = osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id))
            if n:
                if osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), lost_id_status = "COMPLETED"):
                    if osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), lost_id_status = "PROCESSING") or osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), lost_id_status = "PENDING"):
                        data = {'error': True} #sanction already exist
                        return JsonResponse(data, safe=False)
                    else:
                        final = osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), lost_id_status = "PENDING" and "PROCESSING" and "COMPLETED").exclude(lost_id_sanction_excuse = "EXCUSED").count()
                    
                        t = osas_r_code_title.objects.filter(ct_name = "Loss ID / Registration Card")
                        if t:
                            if final == 1:
                                try:
                                    sanction = osas_t_sanction.objects.get(sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "2nd Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_no = stud.stud_id))
                                    data = {'error': True} #sanction already exist
                                    return JsonResponse(data, safe=False)
                                except ObjectDoesNotExist:
                                    try:
                                        obj = osas_r_disciplinary_sanction.objects.get(ds_violation_count = "2nd Offense / Violation", ds_violation_desc = "warning and requiring of 16-hour student-assistance service to be rendered within 5 school days upon report of loss, on top of payment for the cost of ID printing.", ds_hrs = 16, ds_days = 5, ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_status = "Student-assistance Service")

                                        chars = ""
                                        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                        randomstr =''.join((random.choice(chars)) for x in range(8))
                                        random_str = randomstr

                                        today = datetime.today()
                                        lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                                        lost_id.save()
                                        lostid = lost_id.lost_id

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "2nd Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        sanction_id = s.sanction_id
                                        data = {'id': r_id, 'sanction':lostid, 'sanction_id':sanction_id} #disciplinary already exist
                                        return JsonResponse(data, safe=False)

                                    except ObjectDoesNotExist:

                                        obj = osas_r_disciplinary_sanction(ds_violation_count = "2nd Offense / Violation", ds_violation_desc = "warning and requiring of 16-hour student-assistance service to be rendered within 5 school days upon report of loss, on top of payment for the cost of ID printing.", ds_hrs = 16, ds_days = 5, ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_status = "Student-assistance Service")
                                        obj.save()
                                        chars = ""
                                        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                        randomstr =''.join((random.choice(chars)) for x in range(8))
                                        random_str = randomstr

                                        today = datetime.today()
                                        lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                                        lost_id.save()
                                        lostid = lost_id.lost_id

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "2nd Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        sanction_id = s.sanction_id
                                        data = {'id': r_id, 'sanction':lostid, 'sanction_id':sanction_id}
                                        return JsonResponse(data, safe=False)
                            elif final == 2:
                                try:
                                    sanction = osas_t_sanction.objects.get(sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "More Than Two (2) Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_no = stud.stud_id))
                                    data = {'error': True} #sanction already exist
                                    return JsonResponse(data, safe=False)

                                except ObjectDoesNotExist:
                                    try:
                                        obj = osas_r_disciplinary_sanction.objects.get(ds_violation_count = "More Than Two (2) Offense / Violation", ds_violation_desc = "requiring 24-hour student-assistance service to be rendered within 7 schooldays upon report of loss, on top of the payment for the cost of ID printing.", ds_hrs = 24, ds_days = 7, ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_status = "Student-assistance Service")

                                        chars = ""
                                        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                        randomstr =''.join((random.choice(chars)) for x in range(8))
                                        random_str = randomstr

                                        today = datetime.today()
                                        lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                                        lost_id.save()
                                        lostid = lost_id.lost_id

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "More Than Two (2) Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        sanction_id = s.sanction_id
                                        data = {'id': r_id, 'sanction':lostid, 'sanction_id':sanction_id} #disciplinary already exist
                                        return JsonResponse(data, safe=False)

                                    except ObjectDoesNotExist:

                                        obj = osas_r_disciplinary_sanction(ds_violation_count = "More Than Two (2) Offense / Violation", ds_violation_desc = "requiring 24-hour student-assistance service to be rendered within 7 schooldays upon report of loss, on top of the payment for the cost of ID printing.", ds_hrs = 24, ds_days = 7, ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_status = "Student-assistance Service")
                                        obj.save()
                                        chars = ""
                                        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                        randomstr =''.join((random.choice(chars)) for x in range(8))
                                        random_str = randomstr

                                        today = datetime.today()
                                        lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                                        lost_id.save()
                                        lostid = lost_id.lost_id

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "More Than Two (2) Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today)
                                        s.save()
                                        sanction_id = s.sanction_id
                                        data = {'id': r_id, 'sanction':lostid, 'sanction_id':sanction_id}
                                        return JsonResponse(data, safe=False)
                            else:
                                data = {'max': 'reach maximum request'} #reach the maximum request
                                return JsonResponse(data, safe=False)
                                    
                        else:
                            data = {'error': 'code title already exist'} #code title alreadt exist
                            return JsonResponse(data, safe=False)
                else:
                    data = {'error': 'Lost ID record already exist'} #code title alreadt exist
                    return JsonResponse(data, safe=False)
            #if lost id record does not exist
            else:
                t = osas_r_code_title.objects.filter(ct_name = "Loss ID / Registration Card")
                if t:
                    today = datetime.today()
                    lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                    lost_id.save()
                    lostid = lost_id.lost_id
                    chars = ""
                    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                    randomstr =''.join((random.choice(chars)) for x in range(8))
                    random_str = randomstr

                    t = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "1st Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "COMPLETED", sanction_datecreated = today,)
                    t.save()   
                    sanction_id = t.sanction_id

                    data = {'success': True, 'sanction':lostid, 'sanction_id':sanction_id}
                    return JsonResponse(data, safe=False)  
                else:
                    today = datetime.today()
                    lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                    lost_id.save()
                    lostid = lost_id.lost_id

                    chars = ""
                    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                    randomstr =''.join((random.choice(chars)) for x in range(8))
                    random_str = randomstr
                    t = osas_r_code_title(ct_name = "Loss ID / Registration Card")
                    t.save()
                    obj = osas_r_disciplinary_sanction(ds_violation_count = "1st Offense / Violation", ds_violation_desc = "warning and payment for the cost of printing of new ID", ds_hrs = 0, ds_days = 0, ds_code_id = osas_r_code_title.objects.get(ct_name = t.ct_name), ds_status = "WARNING")
                    obj.save()

                    t = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "1st Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "COMPLETED", sanction_datecreated = today)
                    t.save()    
                    sanction_id = t.sanction_id
                    data = {'id': r_id, 'sanction':lostid, 'sanction_id':sanctionid}
                    return JsonResponse(data, safe=False)   
        else:
            data = {'error': 'object'}
            return JsonResponse(data, safe=False) 
    data = {'error': 'object'}
    return JsonResponse(data, safe=False) 

def lost_id_notif_stud(request):
    #change the delete for id and sanction into cancelled
    lost_id_ = request.POST.get('lost_id')
    stud = request.POST.get('stud')
    sanction_id = request.POST.get('sanction_id')
    id_notif = osas_notif(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_lost_id = osas_t_id.objects.get(lost_id = lost_id_), notif_head = "Sent", notif_stat = 'Unseen')
    id_notif.save()
    notif_sanction_id = osas_notif(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id), notif_head = "Sent", notif_stat = 'Unseen')
    notif_sanction_id.save()
    data = {'success': sanction_id}
    return JsonResponse(data, safe=False) 

def lost_id_notif_osas(request):
    #change the delete for id and sanction into cancelled
    stud = request.POST.get('stud')
    lost_id_ = request.POST.get('lost_id')
    sanction_id = request.POST.get('sanction_id')
    id_notif = osas_notif(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_lost_id = osas_t_id.objects.get(lost_id = lost_id_), notif_stud = "Sent", notif_stat = 'Unseen')
    id_notif.save()
    notif_sanction_id = osas_notif(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id), notif_stud = "Sent", notif_stat = 'Unseen')
    notif_sanction_id.save()
    data = {'success': 'true'}
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
    notif = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = "Sent").order_by("-notif_datecreated")
    try:
        profile = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])
        s = profile.stud_birthdate
        n = datetime.strptime(str(s), "%Y-%m-%d").date()
        return render(request, template_name, {'profile': profile, 'n': n, 'notif':notif, 'notif_info':notif_info})
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


#-----------------------------------------SANCTION-----------------------------------------------------
def code_descipline(request):
    ct_list = osas_r_code_title.objects.order_by('ct_id')
    context = {'ct_list': ct_list}
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    return render(request, 'Role_Osas/code_of_descipline.html', {'ct_list': ct_list, 'notif':notif, 'notif_info':notif_info})

def ct_descipline_add(request):
    ct_title = request.POST.get('ct_title')
    t = osas_r_code_title(ct_name = ct_title)
    t.save()
    ct_data = {"id":t.ct_id,"status":t.ct_status, "datecreated":t.ct_datecreated}
    return JsonResponse(ct_data, safe=False)

def ct_descipline_edit(request):
    ct_id = request.POST.get("idInput")
    ct_title = request.POST.get("codeInput")
    try:
        obj = osas_r_code_title.objects.get(ct_id = ct_id)
        obj.ct_name =  ct_title
        obj.save()
        code_data = {"id":obj.ct_id, "code_name": obj.ct_name, "status": obj.ct_status, "datecreated":obj.ct_datecreated}
        data = {'code_data':code_data}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'Role_Osas/code_of_descipline.html')

def ct_descipline_delete(request):
    ct_id = request.POST.get('ct_id')
    try:
        t = osas_r_code_title.objects.get(ct_id = ct_id)
        t.delete()
        data = {'deleted':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'Role_Osas/code_of_descipline.html')

def desciplinary_sanction(request):
    ds_sanction = osas_r_disciplinary_sanction.objects.order_by('ds_violation_count')
    context = {'ds_sanction': ds_sanction}
    code_name = osas_r_code_title.objects.order_by('ct_name').exclude(ct_name = 'Loss ID / Registration Card')
    context2 = {'code_name': code_name}
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    return render(request, 'Role_Osas/desciplinary_sanction.html', {'ds_sanction': ds_sanction, 'code_name': code_name, 'notif':notif, 'notif_info':notif_info})

def desiplinary_sanction_add(request):
    code_name = request.POST.get("code_name")
    offense_name = request.POST.get("offense_name")
    r_hours = request.POST.get("r_hours")
    r_days = request.POST.get("r_days")
    offense_desc = request.POST.get("offense_desc")
    offense_status = request.POST.get("offense_status")

    try:
        d = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_violation_count = offense_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
                
    except ObjectDoesNotExist:
        obj = osas_r_disciplinary_sanction(ds_violation_count = offense_name, ds_violation_desc = offense_desc, ds_hrs = r_hours, ds_days = r_days, ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_status = offense_status)
        obj.save()
        code = osas_r_code_title.objects.get(ct_name = code_name)
        code_title = {'id':code.ct_id}
        sanction_data = {'id':obj.ds_id, 'violation': obj.ds_violation_count, 'descriptions': obj.ds_violation_desc, 'hours':obj.ds_hrs, 'days': obj.ds_days,  'status':obj.ds_status }
        data = {'sanction_data':sanction_data, 'code_title':code_title}
        return JsonResponse(data, safe=False)

def desciplinary_sanction_delete(request):
    sanction_id = request.POST.get("ds_id")
    try:
        obj = osas_r_disciplinary_sanction.objects.get(ds_id = sanction_id)
        obj.delete()
        data = {'deleted':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)
      
def desciplinary_sanction_edit(request):
    r_hours = request.POST.get("r_hours")
    r_days = request.POST.get("r_days")
    offense_desc = request.POST.get("offense_desc")
    offense_status = request.POST.get("offense_status")
    sanction_id = request.POST.get("sanction_id")
    try:
        obj = osas_r_disciplinary_sanction.objects.get(ds_id = sanction_id)
        obj.ds_status = offense_status
        obj.ds_violation_desc = offense_desc
        obj.ds_hrs = r_hours
        obj.ds_days = r_days
        # obj.ds_datecreated = today
        obj.save()
        sanction_data = {'id':obj.ds_id, 'violation': obj.ds_violation_count, 'descriptions': obj.ds_violation_desc, 'hours':obj.ds_hrs, 'days': obj.ds_days,  'status':obj.ds_status }
        data = {'sanction_data':sanction_data}
        return JsonResponse(data, safe=False)
                
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def sanction_excuse_approve(request):
    excuse_id = request.POST.get("excuse_id")
    try:
        r = osas_t_excuse.objects.get(excuse_id = excuse_id)
        r.excuse_status = "APPROVED"
        r.save()
        try:
            t = osas_t_sanction.objects.get(sanction_excuse_id = r.excuse_id)
            t.sanction_status = "EXCUSED"
            t.save()
            if t.sanction_t_id:
                i = osas_t_id.objects.get(lost_id = str(t.sanction_t_id))
                i.lost_id_sanction_excuse = "EXCUSED"
                i.save()
                data = {'success':True}
                return JsonResponse(data, safe=False)
            else:
                data = {'error':True}
                return JsonResponse(data, safe=False)

        except ObjectDoesNotExist:
            data = {'error':True}
            return JsonResponse(data, safe=False)
           
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def sanctioning_role_student(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    notif = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = "Sent").order_by("-notif_datecreated")
    if date1 and date2:
        if status:
            sanction = osas_t_sanction.objects.all().filter(sanction_status = status, sanction_datecreated__range=[date1, date2], sanction_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])).order_by('-sanction_datecreated')
            return render(request, 'Role_Student/sanction.html', {'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
        else:
            sanction = osas_t_sanction.objects.all().filter(sanction_datecreated__range=[date1, date2], sanction_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])).order_by('-sanction_datecreated')
            return render(request, 'Role_Student/sanction.html', {'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
    elif status:
        sanction = osas_t_sanction.objects.all().filter(sanction_status = status, sanction_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])).order_by('-sanction_datecreated')
        return render(request, 'Role_Student/sanction.html', {'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
    else:
        sanction = osas_t_sanction.objects.all().filter(sanction_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])).order_by('-sanction_datecreated')
        return render(request, 'Role_Student/sanction.html', {'sanction':sanction, 'notif':notif, 'notif_info':notif_info})

    

@csrf_exempt
def sanctioning_excuse_add(request):
    sanction_id = request.POST.get("sanction_id")
    excuse = request.POST.get("essay_text")
    stud_no1 = request.session['session_user_no']
    proof = request.FILES.get('image')

    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})')
    cleantext = re.sub(cleanr, '', excuse)

    try:
        t = osas_t_sanction.objects.get(sanction_id = sanction_id)
        if t.sanction_excuse_id:
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            e = osas_t_excuse( 
            excuse_reason = cleantext, 
            excuse_status = "PENDING", 
            excuse_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no1), 
            excuse_proof = proof
            )
            e.save()
            ex_id = e.excuse_id
            try:
                r = osas_t_excuse.objects.get(excuse_id = ex_id)

                ex_id = r.excuse_id
                if ex_id:
                    t.sanction_excuse_id = osas_t_excuse.objects.get(excuse_id = ex_id)
                    t.save()
                    return redirect('/sanctioning_role_student')
                else:
                    return redirect('/sanctioning_role_student')
            except ObjectDoesNotExist:
                data = {'error' :ex_id}
                return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return redirect('/sanctioning_role_student')

def sanctioning_student(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    student = osas_r_personal_info.objects.order_by('stud_no')
    office = osas_r_designation_office.objects.order_by('designation_office')
    descipline = osas_r_disciplinary_sanction.objects.order_by('ds_code_id')
    coc_sunction_list = osas_t_sanction.objects.order_by('sanction_dateupdated')

    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if date1 and date2:
        if status:
            sanction = osas_t_sanction.objects.all().filter(sanction_status = status, sanction_datecreated__range=[date1, date2]).order_by('-sanction_datecreated')
            return render(request, 'Role_Osas/sanctioning.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
        else:
            sanction = osas_t_sanction.objects.all().filter(sanction_datecreated__range=[date1, date2]).order_by('-sanction_datecreated')
            return render(request, 'Role_Osas/sanctioning.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
    elif status:
        sanction = osas_t_sanction.objects.all().filter(sanction_status = status).order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanctioning.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
    else:
        sanction = osas_t_sanction.objects.all().order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanctioning.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction, 'notif':notif, 'notif_info':notif_info})
    


def sanctioning_student_view_excuse(request):
    sanction_excuse_id = request.POST.get('sanction_excuse_id')
    try:
        t = osas_t_excuse.objects.get(excuse_id = sanction_excuse_id)
        e = osas_t_sanction.objects.get(sanction_excuse_id = osas_t_excuse.objects.get(excuse_id = sanction_excuse_id))
        image = json.dumps(str(t.excuse_proof))
        excuse_val = {'id': t.excuse_id, 'status':t.excuse_status,'reason':t.excuse_reason, 'proof':image, 'status':t.excuse_status ,'date':t.excuse_datecreated, 'sanction':e.sanction_code_id.ds_code_id.ct_name}
        data = {'excuse_val':excuse_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def sanctioning_excused_approved(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')

    student = osas_r_personal_info.objects.order_by('stud_no')
    office = osas_r_designation_office.objects.order_by('designation_office')
    descipline = osas_r_disciplinary_sanction.objects.order_by('ds_code_id')
    coc_sunction_list = osas_t_sanction.objects.order_by('sanction_dateupdated')

    if date1 and date2:
        sanction = osas_t_sanction.objects.filter(sanction_status = "EXCUSED",sanction_datecreated__range=[date1, date2]).order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanction_excused.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction}) 
    elif date1:
        sanction = osas_t_sanction.objects.filter(sanction_status = "EXCUSED", sanction_datecreated = date1).order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanction_excused.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction})
    elif date2:
        sanction = osas_t_sanction.objects.filter(sanction_status = "EXCUSED", sanction_datecreated = date2).order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanction_excused.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction})
    else:
        sanction = osas_t_sanction.objects.filter(sanction_status = "EXCUSED" ).order_by('-sanction_datecreated')
        return render(request, 'Role_Osas/sanction_excused.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction})

def sanctioning_student_completed(request):
    sanction2 = osas_t_sanction.objects.filter(sanction_status = "COMPLETED").order_by('-sanction_datecreated')
    student = osas_r_personal_info.objects.order_by('stud_no')
    office = osas_r_designation_office.objects.order_by('designation_office')
    descipline = osas_r_disciplinary_sanction.objects.order_by('ds_code_id')
    coc_sunction_list = osas_t_sanction.objects.order_by('sanction_dateupdated')

    return render(request, 'Role_Osas/sanctioning_completed.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction2':sanction2})

def sanction_student_list(request):
    student_val = list(osas_r_personal_info.objects.values())
    return JsonResponse({'data': student_val})

def sanction_code_list(request):
    code_val = list(osas_r_code_title.objects.values().exclude(ct_name = 'Loss ID / Registration Card'))
    return JsonResponse({'data': code_val})

def designated_office_list(request):
    office_val = list(osas_r_designation_office.objects.values())
    return JsonResponse({'data': office_val})
    
def designation_office_data(request):
    selected_office = request.POST.get('selected_office')
    obj_office = list(osas_r_designation_office.objects.filter(designation_office = selected_office).values())
    return JsonResponse({'data': obj_office})

def sanction_code_data(request):
    selected_code = request.POST.get('selected_code')
    selected_violation = request.POST.get('selected_violation')
    o = osas_r_code_title.objects.get(ct_name = selected_code)
    obj_violation2 = list(osas_r_disciplinary_sanction.objects.filter(ds_code_id__ct_name = o.ct_name,ds_violation_count = selected_violation).values())
    obj_code = list(osas_r_code_title.objects.filter(ct_name = selected_code).values())
    obj_violation = list(osas_r_disciplinary_sanction.objects.filter(ds_code_id__ct_name = o.ct_name).values().order_by('ds_violation_count'))
    return JsonResponse({'data': obj_code, 'obj_violation':obj_violation, 'data3':obj_violation2})

def sanction_student_data(request):
    selected_stud = request.POST.get('selected_stud')
    o = osas_r_personal_info.objects.get(stud_no = selected_stud)
    obj_stud = list(osas_r_personal_info.objects.filter(stud_no = selected_stud).values())
    obj_section = list(osas_r_section_and_year.objects.filter(yas_descriptions = o.stud_yas_id).values())
    obj_course = list(osas_r_course.objects.filter(course_name = o.stud_course_id).values())
    return JsonResponse({'data': obj_stud, 'data2':obj_course, 'data3':obj_section})

def sanction_notif_osas(request):
    #change the delete for id and sanction into cancelled
    stud = request.POST.get('student')
    sanction_id = request.POST.get('sanction_id')
    notif_sanction_id = osas_notif(notif_stud_id = osas_r_personal_info.objects.get(stud_no = stud), notif_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id), notif_stud = "Sent", notif_stat = 'Unseen')
    notif_sanction_id.save()
    data = {'success': 'true'}
    return JsonResponse(data, safe=False)

def sanction_student_add(request):
    today = datetime.today()
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(8))
    auth_id = request.POST.get('auth_id')
    student = request.POST.get('student')
  
    code_name = request.POST.get('code_name')
    violation_name = request.POST.get('violation_name')
    if violation_name == "1st Offense / Violation":
        sanc_status = "COMPLETED"
    else:
        if request.session['session_user_role'] != "HEAD OSAS":
            sanc_status = "PENDING"
        else:
            sanc_status = "ACTIVE"
    office_name = request.POST.get('office_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if office_name == "N/A":
        office_name = "N/A"
    control_number = randomstr
    start_date = request.POST.get('start_date')
    if start_date == "N/A":
        today = None
    s = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_violation_count = violation_name)
    if s:
        try: 
            t = osas_t_sanction.objects.get(sanction_stud_id = osas_r_personal_info.objects.get(stud_no = student), sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_violation_count = violation_name), sanction_status = sanc_status)

            data = {'error':True}
            return JsonResponse(data, safe=False)

        except ObjectDoesNotExist:
            if office_name == "N/A" or start_date == "N/A":
                t = osas_t_sanction(sanction_control_number = control_number, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_violation_count = violation_name),  sanction_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), sanction_stud_id = osas_r_personal_info.objects.get(stud_no = student), sanction_rendered_hr = s.ds_hrs, sanction_status = sanc_status,sanction_datecreated = today)
            else:
                t = osas_t_sanction(sanction_control_number = control_number, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = code_name), ds_violation_count = violation_name),  sanction_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), sanction_stud_id = osas_r_personal_info.objects.get(stud_no = student), sanction_rendered_hr = s.ds_hrs, sanction_status = sanc_status, sanction_datecreated = today, sanction_designation_id = osas_r_designation_office.objects.get(designation_office = office_name), sanction_startdate = start_date, sanction_enddate = end_date)
            t.save()
            a = osas_r_auth_user.objects.get(auth_id = auth_id)
            p = osas_r_personal_info.objects.get(stud_no = student)

            sanction_val = {'id': t.sanction_id, 'control_number':t.sanction_control_number, 'violation':s.ds_violation_count, 'hrs':s.ds_hrs ,'days':s.ds_days,'status':s.ds_status,  'auth':a.auth_id, 'stud_no':p.stud_no, 'rendered_hr':t.sanction_rendered_hr, 'sanc_status':t.sanction_status, 'date':t.sanction_datecreated,}
            data = {'sanction_val':sanction_val}
            return JsonResponse(data, safe=False)
            
    data = {'error':True}
    return JsonResponse(data, safe=False)

def sanction_assign_office(request):
    sanc_id = request.POST.get('sanction_id')
    office = request.POST.get('office')
    try:
        s = osas_t_sanction.objects.get(sanction_designation_id = osas_r_designation_office.objects.get(designation_office = office), sanction_id = sanc_id)
        data = {'error':office}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        s = osas_t_sanction.objects.get(sanction_id = sanc_id)
        s.sanction_designation_id = osas_r_designation_office.objects.get(designation_office = office)
        s.sanction_status = "ACTIVE"
        s.save()
        data = {'success':office}
        return JsonResponse(data, safe=False)
    
def sanction_student_delete(request):
    sanc_id = request.POST.get('sanction_id')
    try:
        t = osas_t_sanction.objects.get(sanction_id = sanc_id)
        if t.sanction_t_id:
            i = osas_t_id.objects.get(lost_id = str(t.sanction_t_id)).delete()
            t.delete()
        else:
            t.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'sanctioning_student.html')

def sanction_student_complete(request):
    sanc_id = request.POST.get('sanction_id')
    try:
        t = osas_t_sanction.objects.get(sanction_id = sanc_id)
        t.sanction_status = "COMPLETED"
        t.sanction_rendered_hr = t.sanction_code_id.ds_hrs
        t.sanction_excuse_id = None
        t.save()
        data = {'success':t.sanction_rendered_hr}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'sanctioning_student.html')

def sanction_student_view(request):
    today = datetime.today()
    sanc_id = request.POST.get('sanction_id')
    t = osas_t_sanction.objects.get(sanction_id = sanc_id)
    if t.sanction_designation_id:
        office_name = t.sanction_designation_id.designation_office
        try:
            s = osas_r_designation_office.objects.get(designation_office = office_name)
            office = s.designation_office
            start = t.sanction_startdate
            end = t.sanction_enddate

        except ObjectDoesNotExist:
            office = "N/A"
            start = "N/A"
            end = "N/A"
    else:
        office = "N/A"
        start = "N/A"
        end = "N/A"
    sanction_val = {
        #sanction data
        'id': t.sanction_id,
        'control_number':t.sanction_control_number, 
        'rendered_hour':t.sanction_rendered_hr,
        'sanc_status':t.sanction_status,  
        'start':start,
        'end':end,
        'datecreated':t.sanction_datecreated,
        #student data
        'stud_no': t.sanction_stud_id.stud_no, 
        'contact': t.sanction_stud_id.stud_m_number, 
        'stud_lname': t.sanction_stud_id.stud_lname, 
        'stud_fname': t.sanction_stud_id.stud_fname,
        'stud_mname': t.sanction_stud_id.stud_mname,
        'stud_course': t.sanction_stud_id.stud_course_id.course_name,
        'stud_year': t.sanction_stud_id.stud_yas_id.yas_descriptions,
        #desciplinary data
        'sanction_name':t.sanction_code_id.ds_code_id.ct_name, 
        'violation':t.sanction_code_id.ds_violation_count,
        'desc':t.sanction_code_id.ds_violation_desc,
        'violation_status':t.sanction_code_id.ds_status,
        'hrs':t.sanction_code_id.ds_hrs,
        'days':t.sanction_code_id.ds_days,
        #office data
        'office':office,
        }
    data = {'sanction_val':sanction_val}
    return JsonResponse(data, safe=False)
   

def designation_office(request):
    office_list = osas_r_designation_office.objects.order_by('designation_id')
    context = {'office_list': office_list}
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    return render(request, 'designation_office.html', {'office_list': office_list, 'notif':notif, 'notif_info':notif_info})

def designation_office_add(request):
    office = request.POST.get("officeInput")
    try:
        obj = osas_r_designation_office(designation_office = office)
        obj.save()
        office_data = {"id":obj.designation_id, "office_name": obj.designation_office, "datecreated":obj.designation_datecreated}
        data = {'office_data':office_data}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'designation_office.html')

def designation_office_edit(request):
    office_id = request.POST.get("idInput")
    office = request.POST.get("officeInput")
    try:
        obj = osas_r_designation_office.objects.get(designation_id = office_id)
        obj.designation_office =  office
        obj.save()
        office_data = {"id":obj.designation_id, "office_name": obj.designation_office, "datecreated":obj.designation_datecreated}
        data = {'office_data':office_data}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'designation_office.html')

def designation_office_delete(request):
    office_id = request.POST.get("designation_id")
    try:
        o = osas_r_designation_office.objects.get(designation_id = office_id)
        o.delete()
        data = {'deleted':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return render(request, 'designation_office.html')

def lodge_complaint(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    category = request.POST.get('filter_cat')
    notif = osas_notif.objects.all().filter(notif_head = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_head = "Sent").order_by("-notif_datecreated")
    if status and category:
        stud_complaints = osas_t_complaint.objects.all().filter(comp_status = status, comp_category = category).order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    if date1 and date2:
        if status:
            stud_complaints = osas_t_complaint.objects.all().filter(comp_status = status, comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
        elif category:
            stud_complaints = osas_t_complaint.objects.all().filter(comp_category = category, comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
        else:
            stud_complaints = osas_t_complaint.objects.all().filter(comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    elif status:
        stud_complaints = osas_t_complaint.objects.all().filter(comp_status = status).order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    elif category:
        stud_complaints = osas_t_complaint.objects.all().filter(comp_category = category).order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    elif date1:
        stud_complaints = osas_t_complaint.objects.all().filter(comp_datecreated = date1).order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    elif date2:
        stud_complaints = osas_t_complaint.objects.all().filter(comp_datecreated = date2).order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    else:
        stud_complaints = osas_t_complaint.objects.all().order_by('-comp_datecreated')
        return render(request, 'Role_Osas/lodge_complaint.html', { 'stud_complaints':stud_complaints, 'notif':notif, 'notif_info':notif_info})
    

def student_file_complaint(request):
    date1 = request.POST.get('date_from')
    date2 = request.POST.get('date_to')
    status = request.POST.get('filter_status')
    category = request.POST.get('filter_cat')
    student_course = osas_r_course.objects.order_by('course_name')
    notif = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = 'Sent').count()
    notif_info = osas_notif.objects.all().filter(notif_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), notif_stud = "Sent").order_by("-notif_datecreated")
    if date1 and date2:
        if status:
            stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_status = status, comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
        elif category:
            stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_category = category, comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
        else:
            stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_datecreated__range=[date1, date2]).order_by('-comp_datecreated')
            return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
    elif status and category:
        stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_status = status, comp_category = category).order_by('-comp_datecreated')
        return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
    elif status:
        stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_status = status).order_by('-comp_datecreated')
        return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
    elif category:
        stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']), comp_category = category).order_by('-comp_datecreated')
        return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})
    else:
        stud_complaint = osas_t_complaint.objects.all().filter(comp_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no'])).order_by('-comp_datecreated')
        return render(request, 'Role_Student/file_a_complaint.html', {'stud_complaint':stud_complaint, 'student_course':student_course, 'notif':notif, 'notif_info':notif_info})

def student_file_complaint_get(request):
    comp_id = request.POST.get('comp_id')
    try:
        c = osas_t_complaint.objects.get(comp_id = comp_id)
        image = json.dumps(str(c.comp_pic))
        if request.session['session_user_role'] == "HEAD OSAS":
            c.comp_seen = "Seen"
            c.save()
        comp_val = {"id":c.comp_id, "number":c.comp_number, 'letter':c.comp_letter, 'pic':image, 'status':c.comp_status, 'stud':c.comp_stud_id.stud_no, 'lname':c.comp_stud_id.stud_lname, 'fname':c.comp_stud_id.stud_fname, 'mname':c.comp_stud_id.stud_mname , 'course':c.comp_stud_id.stud_course_id.course_name, 'date':c.comp_datecreated}
        data = {'comp_val':comp_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def student_file_complaint_edit(request):
    comp_id = request.POST.get('comp_id')
    letter = request.POST.get('letter')
    try:
        c = osas_t_complaint.objects.get(comp_id = comp_id, comp_status = "PENDING", comp_seen = None)
        c.comp_letter = letter
        today = datetime.today()
        c.comp_datecreated = today
        c.save()
        data = {'success':"success"}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':"error"}
        return JsonResponse(data, safe=False)

def student_file_complaint_add(request):
    dd_course = request.POST.get('dd_course')
    g_lname = request.POST.get('g_lname')
    g_fname = request.POST.get('g_fname')
    g_mname = request.POST.get('g_mname')

    letter = request.POST.get('essay_text')
    stud_no = request.session['session_user_no']
    category = request.POST.get('g_category')
    nature_complaint = request.POST.get('n_complaint')
    if dd_course and g_lname and g_fname:
        g_assign = g_fname + " " + g_mname + " " + g_lname
    else:
        g_assign = request.POST.get('g_assig')
    proof_image = request.FILES.get('p_image')
    chars = ""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(8))
    random_str = randomstr
    try:
        c = osas_t_complaint.objects.get(comp_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), comp_status = "PENDING")
        messages.error(request, 'Complaint cannot be send while you have a pending complaint')
        return HttpResponseRedirect('/student_file_complaint')  
    except ObjectDoesNotExist:
        c = osas_t_complaint(comp_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), comp_number = random_str, comp_letter = letter, comp_pic = proof_image, comp_category = category, comp_nature = nature_complaint, comp_g_assign = g_assign)
        comp_id = c.comp_id
        c.save()
        return HttpResponseRedirect('/student_file_complaint')  

def student_file_complaint_check(request):
    dd_course = request.POST.get('dd_course')
    g_lname = request.POST.get('g_lname')
    g_fname = request.POST.get('g_fname')
    g_mname = request.POST.get('g_mname')
    try:
        if g_mname:
            s = osas_r_personal_info.objects.get(stud_course_id = osas_r_course.objects.get(course_name = dd_course), stud_lname = g_lname, stud_fname = g_fname, stud_mname = g_mname)
            data = {'success':True}
            return JsonResponse(data, safe=False)
        else:
            s = osas_r_personal_info.objects.get(stud_course_id = osas_r_course.objects.get(course_name = dd_course), stud_lname = g_lname, stud_fname = g_fname)
            data = {'success':True}
            return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def student_file_complaint_add_proof(request):
    proof_image = request.FILES.get('image')
    stud_no = request.session['session_user_no']
    try:
        c = osas_t_complaint.objects.get(comp_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), comp_status = "PENDING")
        c.comp_pic = proof_image
        c.save()
        data = {'success':True}
        time.sleep(1)
        return HttpResponseRedirect('/student_file_complaint') 
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def student_file_complaint_edit_proof(request):
    proof_image = request.FILES.get('image1')
    stud_no = request.session['session_user_no']
    try:
        c = osas_t_complaint.objects.get(comp_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no), comp_status = "PENDING", comp_seen = None)
        if proof_image:
            proof_img = request.FILES.get('image1')
            c.comp_pic = proof_img
            today = datetime.today()
            c.comp_datecreated = today
            c.save()
        data = {'success':True}
        time.sleep(.7)
        return HttpResponseRedirect('/student_file_complaint') 
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/student_file_complaint')  

def student_file_complaint_remove(request):
    comp_id = request.POST.get('comp_id')
    try:
        osas_t_complaint.objects.get(comp_id = comp_id, comp_status = "PENDING").delete()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': r_id}
        return JsonResponse(data, safe=False)

def lodge_complaint_approve(request):
    comp_id = request.POST.get('comp_id')
    stats = request.POST.get('status')
    try:
        if stats == "APPROVED":
            t = osas_t_complaint.objects.get(comp_id = comp_id, comp_status = "PENDING")
            t.comp_status = "APPROVED"
        elif stats == "DECLINED":
            t = osas_t_complaint.objects.get(comp_id = comp_id, comp_status = "PENDING")
            t.comp_status = "DECLINED"
        t.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/student_file_complaint')  
    
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

def organization_osas(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    stud_list = osas_r_personal_info.objects.all().order_by("stud_no")
    year = str(acad_year)
    if acad_year and status:
        org_list = organization.objects.all().filter(org_status = status, org_datecreated__contains =  year).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list})
    elif acad_year:
        org_list = organization.objects.all().filter(org_datecreated__contains =  year).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list})
    elif status:
        org_list = organization.objects.all().filter(org_status = status ).order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list})
    else:   
        org_list = organization.objects.all().order_by('org_datecreated')
        return render(request, 'Facilitation/organization.html', {'org_list':org_list, 'stud_list':stud_list})
        
def organization_osas_classroom(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    stud_list = osas_r_personal_info.objects.all().order_by("stud_no")
    year = str(acad_year)
    if acad_year and status:
        org_list = classroom.objects.all().filter(room_status = status, room_datecreated__contains =  year).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list})
    elif acad_year:
        org_list = classroom.objects.all().filter(room_datecreated__contains =  year).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list})
    elif status:
        org_list = classroom.objects.all().filter(room_status = status ).order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list})
    else:   
        org_list = classroom.objects.all().order_by('room_datecreated')
        return render(request, 'Facilitation/classroom.html', {'org_list':org_list, 'stud_list':stud_list})


def organization_osas_new_class_account(request):
    stud = request.POST.get('stud')
    class_year = request.POST.get('class_year')
    class_sec = request.POST.get('class_sec')
    class_email = request.POST.get('class_email')
    class_pass = request.POST.get('class_pass')
    try:
        org = classroom.objects.get(room_year = class_year, room_sec = class_sec, room_email = class_email, room_stud_id = osas_r_personal_info.objects.get(stud_no = stud))
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        today = datetime.today()
        year = timedelta(days=365)
        room_datecreated = today
        room_expiration = today + year
        room = classroom( 
            room_year = class_year,
            room_sec = class_sec, 
            room_email = class_email, 
            room_pass = class_pass, 
            room_stud_id = osas_r_personal_info.objects.get(stud_no = stud), 
            room_datecreated = room_datecreated,
            room_expiration = room_expiration,
            )
        room.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)

def organization_new_account(request):
    stud = request.POST.get('stud')
    org_name = request.POST.get('org_name')
    org_abbr = request.POST.get('org_abbr')
    org_email = request.POST.get('org_email')
    org_pass = request.POST.get('org_pass')
    try:
        org = organization.objects.get(org_name = org_name, org_abbr = org_abbr, org_email = org_email, org_stud_id = osas_r_personal_info.objects.get(stud_no = stud))
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        today = datetime.today()
        year = timedelta(days=365)
        org_date_accredited = today
        org_date_accredited_year = today
        org_expiration = today + year
        org = organization( 
            org_name = org_name,
            org_abbr = org_abbr, 
            org_email = org_email, 
            org_pass = org_pass, 
            org_stud_id = osas_r_personal_info.objects.get(stud_no = stud), 
            org_status = 'ACCREDITED', 
            org_date_accredited = org_date_accredited,
            org_expiration = org_expiration,
            org_date_accredited_year = org_date_accredited_year,
            org_submit_date = today
            )
        org.save()
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
    try:
        d = concept_paper_title.objects.get(title_id = title_id)
        if stats == "PENDING":
            d.title_status = 'VALIDATED'
            d.save()
        else:
            d.title_status = 'APPROVED'
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
   
    # osas_role_id = osas_r_auth_user.objects.get(auth_id = osas_r_userrole.objects.get(user_type = "HEAD OSAS"))
    return JsonResponse({
        'data': messages_list,
        'org_data':org_id.org_abbr,
        'org_id':org_id.org_abbr,
        'org_msg_status':org_id.org_abbr,
        'osas_data':osas_id.auth_role.user_type,
        'osas_role_id':osas_role.auth_id,
        'osas_role':osas_role.auth_role.user_type,
        # 'osas_id':osas_role.auth_id
    })

def class_view_messages(request):
    room_id = request.POST.get('room_id')
    messages_list = list(organization_chat.objects.all().values())
    room_id = classroom.objects.get(room_id = room_id)
    osas_role = osas_r_auth_user.objects.get(auth_role = osas_r_userrole.objects.get(user_type = "HEAD OSAS"))
    osas_id = osas_r_auth_user.objects.get(auth_id = osas_role.auth_id)
   
    # osas_role_id = osas_r_auth_user.objects.get(auth_id = osas_r_userrole.objects.get(user_type = "HEAD OSAS"))
    return JsonResponse({
        'data': messages_list,
        'room_id':room_id.room_id,
        'room_year':room_id.room_year,
        'room_sec':room_id.room_sec,
        'room_course':room_id.room_stud_id.stud_course_id.course_name,
        'osas_data':osas_id.auth_role.user_type,
        'osas_role_id':osas_role.auth_id,
        'osas_role':osas_role.auth_role.user_type,
        # 'osas_id':osas_role.auth_id
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
            o = org_concept_paper.objects.get(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_file = docu, con_org_id = organization.objects.get(org_id = pk_id))
            o.delete()
            org_concept_paper.objects.create(con_file = docu, con_org_id = organization.objects.get(org_id = pk_id), con_file_ext = extension, con_status = "APPROVED", con_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), con_title_id = concept_paper_title.objects.get(title_id = title_id))
            return HttpResponse('')
        elif ident == 'class':
            o = org_concept_paper.objects.get(con_title_id = concept_paper_title.objects.get(title_id = title_id), con_file = docu, con_room_id = classroom.objects.get(room_id = pk_id))
            o.delete()
            org_concept_paper.objects.create(con_file = docu, con_room_id = classroom.objects.get(room_id = pk_id), con_file_ext = extension, con_status = "APPROVED" , con_auth_id = osas_r_auth_user.objects.get(auth_id = auth_id), con_title_id = concept_paper_title.objects.get(title_id = title_id))
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
    return render(request, 'Organization/home.html')

def classroom_home(request):
    return render(request, 'classroom/home.html')

def organiation_login_process(request):
    s_no = request.POST.get('stud_no')
    password = request.POST.get('pass')
    try:
        c = organization.objects.get(org_email=s_no)
        org = organization.objects.filter(org_email=s_no, org_pass= password)
        # s = osas_r_userrole.objects.get(user_id= stud.stud_role)
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


def accreditation(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    year = str(acad_year)
    d = organization.objects.filter(org_id = request.session['session_user_id'])
    if acad_year and status:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_status = status, acc_datecreated__contains = year ).order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'd':d})
    elif status:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_status = status).order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'd':d})
    elif acad_year:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_datecreated__contains = year ).order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'd':d})
    else:
        files = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id']),acc_status = "SAVED").order_by('-acc_datecreated')
        return render(request, 'Organization/accreditation.html', {'files':files, 'd':d})

def accreditation_upload(request):
    docu = request.FILES.get('file')
    if request.method == 'POST':
        p = org_accreditation.objects.filter(acc_org_id = organization.objects.get(org_id = request.session['session_user_id'])).count()
        if p < 8:
            org_accreditation.objects.create(acc_file = docu, acc_org_id = organization.objects.get(org_id = request.session['session_user_id']), acc_doc_type = docu)
            return HttpResponse('')
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
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_status = "PENDING", title_room_id = classroom.objects.get(room_id = room_id))
        data = {'success':True}
        return JsonResponse(data, safe=False)

def org_concept_paper_title(request):
    title_name = request.POST.get('con_title')
    org_id = request.POST.get('org_id')
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_status = "PENDING", title_org_id = organization.objects.get(org_id = room_id))
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
    org_id = request.POST.get('org_id')
    try:
        t = concept_paper_title.objects.get(title_name = title_name)
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        concept_paper_title.objects.create(title_name = title_name, title_status = "PENDING", title_org_id = organization.objects.get(org_id = org_id))
        data = {'success':True}
        return JsonResponse(data, safe=False)

def accreditation_document_delete(request):
    doc_id = request.POST.get('doc_id')
    org_id = request.POST.get('org_id')
    btn_status = request.POST.get('btn_status')
    try:
        d = org_accreditation.objects.get(acc_id = doc_id)
        e = organization.objects.get(org_id = org_id)
        if e.org_status == 'ACCREDITED':
            data = {'error':True}
            return JsonResponse(data, safe=False)
        else:
            if btn_status == "Remove File(s)":
                d.delete()
            elif btn_status == "Retrieve File(s)":
                d.acc_status = "SAVED"
                d.save()
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
    class_name = course_name + ' ' + class_year + ' - ' + class_sec
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
    class_name = course_name + ' ' + class_year + ' - ' + class_sec
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
        # s = role.auth_role.user_type
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

def organization_fund(request):
    return render(request, 'Organization/fund.html')

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
        if p < 8:
            org_concept_paper.objects.create(con_file = docu, con_room_id = classroom.objects.get(room_id = request.session['session_user_id']), con_file_ext = extension, con_status = 'SENT', con_title_id = concept_paper_title.objects.get(title_id = title_id2))
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
    file_list = concept_paper_title.objects.all()
    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        acc_list = organization.objects.all().filter(org_status = status, org_date_accredited__contains = year).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    elif acad_year:
        acc_list = organization.objects.all().filter(org_date_accredited__contains = year).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    if status:
        acc_list = organization.objects.all().filter(org_status = status ).order_by("-org_date_accredited")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Facilitation/concept_papers.html', {'acc_list':acc_list, 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list':file_list})
    else:
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
    file_list_room = concept_paper_title.objects.all().filter(title_room_id = classroom.objects.get(room_id = request.session['session_user_id']))
    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        file_list = concept_paper_title.objects.all().filter(title_status = status, title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    elif acad_year:
        file_list = concept_paper_title.objects.all().filter( title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', { 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    if status:
        file_list = concept_paper_title.objects.all().filter(title_status = status).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})
    else:
        file_list = concept_paper_title.objects.all().order_by("-title_datecreated")
        class_list = classroom.objects.all().order_by("-room_datecreated")
        return render(request, 'classroom/student_events.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_room':file_list_room})

def organization_events(request):
    status = request.POST.get('filter_status')
    acad_year = request.POST.get('acad_year')
    acc_docu_list = org_concept_paper.objects.all().filter(con_status = 'SENT')
    file_list_org = concept_paper_title.objects.all().filter(title_org_id = organization.objects.get(org_id = request.session['session_user_id']))
    osas_docu_list = org_concept_paper.objects.all().filter(con_status = 'APPROVED')
    acc_docu = org_concept_paper.objects.all().order_by("con_id")
    year = str(acad_year)

    msg = organization_chat.objects.all().order_by('msg_date')

    if acad_year and status:
        file_list = concept_paper_title.objects.all().filter(title_status = status, title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    elif acad_year:
        file_list = concept_paper_title.objects.all().filter( title_datecreated__contains = year).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', { 'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    if status:
        file_list = concept_paper_title.objects.all().filter(title_status = status).order_by("-title_datecreated")
        class_list = classroom.objects.all().filter( room_datecreated__contains = year).order_by("-room_datecreated")
        return render(request, 'Organization/organization_event.html', {'acc_docu':acc_docu, 'acc_docu_list':acc_docu_list, 'msg':msg, 'class_list':class_list, 'osas_docu_list':osas_docu_list, 'file_list_org':file_list_org})
    else:
        file_list = concept_paper_title.objects.all().order_by("-title_datecreated")
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
        
