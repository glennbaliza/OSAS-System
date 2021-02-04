import random
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import osas_r_userrole, osas_r_course, osas_r_section_and_year, osas_r_personal_info, osas_r_auth_user, osas_t_id, osas_t_sanction, osas_r_code_title, osas_r_disciplinary_sanction, osas_r_designation_office, osas_t_excuse
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime, date, timedelta
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
import re
import json
@cache_control(no_cache=True, must_revalidate=True, no_store=True)




def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_templte.html', data)
		return HttpResponse(pdf, content_type='application/pdf')



def home(request):
    return render(request, 'home.html', {})

def dashboard(request):
    return render(request, 'Role_Student/dashboard.html', {})
#--------------------------------------LOGIN------------------------------------------------------------------------------------------
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
                s = osas_r_userrole.objects.get(user_type=stud.stud_role)
                request.session['session_user_id'] = stud.stud_id
                request.session['session_user_no'] = stud.stud_no
                request.session['session_user_lname'] = stud.stud_lname
                request.session['session_user_fname'] = stud.stud_fname
                request.session['session_user_pass'] = stud.s_password
                request.session['session_user_role'] = s.user_type
                return HttpResponseRedirect('/dashboard', {'stud': stud}) #passing the values of student to the next template
        else:
            messages.error(request, 'Either student number or password are incorrect.')
            return HttpResponseRedirect('/login')
    except ObjectDoesNotExist:
        u = osas_r_auth_user.objects.filter(auth_username=s_no).count()
        if u:
            r = osas_r_auth_user.objects.get(auth_username=s_no)
            f = osas_r_userrole.objects.get(user_id=r.auth_id)
            if r.auth_username == s_no and r.auth_password == password:
                if r.auth_role_id == 2:
                    request.session['session_user_id'] = r.auth_id
                    request.session['session_user_lname'] = r.auth_lname
                    request.session['session_user_fname'] = r.auth_fname
                    request.session['session_user_username'] = r.auth_username
                    request.session['session_user_pass'] = r.auth_password
                    request.session['session_user_role'] = f.user_type
                    return HttpResponseRedirect('/home')
                else: 
                    request.session['session_user_id'] = r.auth_id
                    request.session['session_user_lname'] = r.auth_lname
                    request.session['session_user_fname'] = r.auth_fname
                    request.session['session_user_username'] = r.auth_username
                    request.session['session_user_pass'] = r.auth_password
                    request.session['session_user_role'] = f.user_type
                    return HttpResponseRedirect('/home')
            else: 
                messages.error(request, 'Incorrect username or password, please try again.')
                return HttpResponseRedirect('/login')
        else:
            messages.error(request, 'Incorrect username or password, please try again.')
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
                            stud.stud_status = 'Active'
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
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
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
    stud_pass = randomstr
    try:
        n = osas_r_personal_info.objects.get(stud_no = studno)
        return HttpResponseRedirect('/student_profile' , {'error_message': "Duplicated Course Information : " + studno})
    except ObjectDoesNotExist:
        today = datetime.today()
        stud = osas_r_personal_info(stud_no = studno, stud_lname = l_name, stud_fname = f_name, stud_mname = m_name, stud_birthdate = d_of_birth,stud_gender = gender, stud_address = address, stud_email = email, stud_m_number = mobile_number, stud_hs = h_name, stud_hs_add = h_address, stud_e_name = e_name,stud_e_address = e_address, stud_e_m_number = e_number, s_password = stud_pass , date_created = today, stud_role = osas_r_userrole.objects.get(user_type='STUDENT'), stud_course_id = osas_r_course.objects.get(course_name = course), stud_yas_id  = osas_r_section_and_year.objects.get(yas_descriptions = yr_sec))
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

def deleteuser(request):
    id = request.POST.get('del_user_id')
    osas_r_userrole.objects.get(pk=id).delete()
    return HttpResponseRedirect('/userrole')

def auth_user(request):
    template_name = 'auth_user.html'
    auth_user = osas_r_auth_user.objects.order_by('auth_username')
    userrole = osas_r_userrole.objects.order_by('user_type')
    return render(request, template_name, {'auth_user': auth_user, 'userrole':userrole })

def auth_process_edit(request, auth_id):
    template_name = 'auth_process_edit.html'
    # auth = osas_r_auth_user.objects.order_by('auth_username')
    role = osas_r_userrole.objects.order_by('user_type')
    try:
        auth_user = osas_r_auth_user.objects.get(auth_id=auth_id)
    except osas_r_auth_user.DoesNotExist:
            raise Http404("User profile does not exist")
    return render(request, template_name,{'auth_user':auth_user, 'role': role})

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
    _lname = request.POST.get('auth_lname')
    _fname = request.POST.get('auth_fname')
    _username = request.POST.get('auth_username')
    _pass = request.POST.get('auth_pass')
    _pass1 = request.POST.get('aut_pass1')
    _user = request.POST.get('auth_user')
    try:
        n = osas_r_auth_user.objects.get(auth_username=_username)
        messages.error(request, _username +  ' ' + 'is already exist.')
        return redirect('/auth_user')
    except ObjectDoesNotExist:
        today = datetime.today()
        if _user:
            if _pass == _pass1:
                user = osas_r_auth_user.objects.create(auth_lname=_lname,auth_fname=_fname, auth_username=_username, auth_password=_pass, auth_role=osas_r_userrole.objects.get(user_type=_user),date_created=today)
                # user.save()
                messages.success(request, _username + ' ' +  'Successfully Added!')
                return redirect('/auth_user')
            else:
                messages.success(request, 'Password does not match!')
                return redirect('/auth_user')
        else:
            messages.error(request, _username + ' ' + 'is already taken.')
            return render(request, 'auth_user.html')


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
    stud_info =  osas_t_id.objects.filter(lost_stud_id = request.session['session_user_id'])
    return render(request, 'Role_Student/student_lost_id.html', {'stud_info': stud_info})
#-----------------------------ID---------------------------------------------------------------------------
def lost_id(request):
    stud_list = osas_t_id.objects.filter(lost_id_status = 'COMPLETE') # queryset for all existing student_no
    stud_ = osas_r_personal_info.objects.all()
    stud_list2 = osas_r_personal_info.objects.filter(stud_id__in = stud_.values_list('stud_id',)) # queryset for all the student then exclude the data that existing in the osas_t_id
    id_request =  osas_t_id.objects.exclude(lost_id_status = 'CANCELLED').order_by('-date_created')
    pending_list =  osas_t_id.objects.filter(lost_id_status = 'PENDING').order_by('-date_created')
    process_list =  osas_t_id.objects.filter(lost_id_status = 'PROCESSING').order_by('-date_created')
    complete_list =  osas_t_id.objects.filter(lost_id_status = 'COMPLETED').order_by('-date_created')
    return render(request, 'id/lost_id.html', {'stud_list2': stud_list2, 'complete_list': complete_list, 'pending_list': pending_list, 'process_list': process_list, 'id_request': id_request, 'stud_list':stud_list})

def id_request_process(request):
    r_id = request.POST.get('lost_id')
    status = request.POST.get('status')
    
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
        data = {'error': id_request}
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
        s = osas_t_id.objects.get(lost_id = r_id)
        s.lost_id_status = "CANCELLED"
        s.save()
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
                    if osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), lost_id_status = "PROCESSING"):
                        data = {'error': True} #sanction already exist
                        return JsonResponse(data, safe=False)
                    else:
                        count = osas_t_id.objects.filter(lost_stud_id = osas_r_personal_info.objects.get(stud_no = no)).exclude(lost_id_status = "COMPLETED" and "CANCELLED").count()
                        t = osas_r_code_title.objects.filter(ct_name = "Loss ID / Registration Card")
                        if t:
                            if count == 1:
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

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "2nd Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        
                                        data = {'id': r_id, 'sanction':random_str} #disciplinary already exist
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
                                    

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "2nd Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        
                                        data = {'id': r_id, 'sanction':random_str}
                                        return JsonResponse(data, safe=False)
                            elif count == 2:
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

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "More Than Two (2) Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today,)
                                        s.save()

                                        
                                        data = {'id': r_id, 'sanction':random_str} #disciplinary already exist
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

                                        s = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "More Than Two (2) Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "PENDING", sanction_datecreated = today)
                                        s.save()

                                        data = {'id': r_id, 'sanction':random_str}
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
                    
                    chars = ""
                    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                    randomstr =''.join((random.choice(chars)) for x in range(8))
                    random_str = randomstr

                    t = osas_t_sanction(sanction_t_id = osas_t_id.objects.get(request_id = r_id), sanction_control_number = random_str, sanction_code_id = osas_r_disciplinary_sanction.objects.get(ds_code_id = osas_r_code_title.objects.get(ct_name = "Loss ID / Registration Card"), ds_violation_count = "1st Offense / Violation"), sanction_stud_id = osas_r_personal_info.objects.get(stud_id = stud.stud_id), sanction_rendered_hr = 0, sanction_status = "COMPLETED", sanction_datecreated = today,)
                    t.save()    

                    data = {'error': True, 'sanction':random_str}
                    return JsonResponse(data, safe=False)  
                else:
                    today = datetime.today()
                    lost_id = osas_t_id(request_id = r_id, lost_stud_id = osas_r_personal_info.objects.get(stud_no = no), date_created = today, date_updated=today)
                    lost_id.save()

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
                    data = {'id': r_id, 'sanction':random_str}
                    return JsonResponse(data, safe=False)   
                   
                         
        else:
            data = {'error': 'object'}
            return JsonResponse(data, safe=False) 
    data = {'error': 'object'}
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
        messages.success(request, str(s), 'Successfully Updated!')
        return HttpResponseRedirect('/profile')


#-----------------------------------------SANCTION-----------------------------------------------------
def code_descipline(request):
    ct_list = osas_r_code_title.objects.order_by('ct_id')
    context = {'ct_list': ct_list}
    return render(request, 'Role_Osas/code_of_descipline.html', {'ct_list': ct_list})

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
    return render(request, 'Role_Osas/desciplinary_sanction.html', {'ds_sanction': ds_sanction, 'code_name': code_name})

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

def sanctioning_role_student(request):
    sanction = osas_t_sanction.objects.filter(sanction_stud_id = osas_r_personal_info.objects.get(stud_no = request.session['session_user_no']))
    return render(request, 'Role_Student/sanction.html', {'sanction':sanction})
    
@csrf_exempt
def sanctioning_excuse_add(request):
    
    sanction_id = request.POST.get("sanction_id")
    excuse = request.POST.get("essay_text")
    stud_no1 = request.session['session_user_no']
    proof = request.FILES.get('image')

    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})')
    cleantext = re.sub(cleanr, '', excuse)

    try:
        t = osas_t_excuse.objects.get(excuse_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no1),excuse_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id), excuse_status = "PENDING" )
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        t = osas_t_excuse( 
            excuse_reason = cleantext, 
            excuse_status = "PENDING", 
            excuse_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no1), 
            excuse_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id),
            excuse_proof = proof
        )
        t.save()
        p = osas_t_excuse.objects.get(excuse_stud_id = osas_r_personal_info.objects.get(stud_no = stud_no1),excuse_sanction_id = osas_t_sanction.objects.get(sanction_id = sanction_id))
        e = osas_t_sanction.objects.get(sanction_id = sanction_id)
        e.sanction_excuse_id = osas_t_excuse.objects.get(excuse_id = p.excuse_id)
        e.save()
        return redirect('/sanctioning_role_student')

def sanctioning_student(request):
    sanction = osas_t_sanction.objects.exclude(sanction_status = "COMPLETED").order_by('-sanction_datecreated')
    student = osas_r_personal_info.objects.order_by('stud_no')
    office = osas_r_designation_office.objects.order_by('designation_office')
    descipline = osas_r_disciplinary_sanction.objects.order_by('ds_code_id')
    coc_sunction_list = osas_t_sanction.objects.order_by('sanction_dateupdated')

    return render(request, 'Role_Osas/sanctioning.html', {'coc_sunction_list':coc_sunction_list, 'descipline':descipline, 'student':student, 'office':office, 'sanction':sanction})

def sanctioning_student_view_excuse(request):
    sanction_excuse_id = request.POST.get('sanction_excuse_id')
    try:
        t = osas_t_excuse.objects.get(excuse_id = sanction_excuse_id)
        image = json.dumps(str(t.excuse_proof))
        excuse_val = {'id': t.excuse_id, 'reason':t.excuse_reason, 'proof':image, 'status':t.excuse_status ,'date':t.excuse_datecreated, 'sanction':t.excuse_sanction_id.sanction_code_id.ds_code_id.ct_name}
        data = {'excuse_val':excuse_val}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

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

def sanction_student_add(request):
    today = datetime.today()
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    auth_id = request.POST.get('auth_id')
    student = request.POST.get('student')
    code_name = request.POST.get('code_name')
    violation_name = request.POST.get('violation_name')
    if violation_name == "1st Offense / Violation":
        sanc_status = "Completed"
    else:
        sanc_status = "Active"
    office_name = request.POST.get('office_name')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if office_name == "N/A":
        office_name = "N/A"
    control_number = "SS-" + randomstr
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
    return render(request, 'designation_office.html', {'office_list': office_list})

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

