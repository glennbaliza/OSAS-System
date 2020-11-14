import random
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import osas_r_userrole, osas_r_course, osas_r_section_and_year, osas_r_personal_info, osas_r_referral, osas_r_auth_user
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def home(request):
    return render(request, 'home.html', {})
#--------------------------------------LOGIN------------------------------------------------------------------------------------------
def login(request):
    try:
        del request.session['session_user_role']
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
                messages.success(request, s_no + ' Log in as ' + str(stud.stud_role))
                request.session['session_user_id'] = stud.stud_id
                request.session['session_user_no'] = stud.stud_no
                request.session['session_user_lname'] = stud.stud_lname
                request.session['session_user_fname'] = stud.stud_fname
                request.session['session_user_pass'] = stud.s_password
                request.session['session_user_role'] = s.user_type
                return HttpResponseRedirect('/home', {'stud': stud}) #passing the values of student to the next template
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
                    messages.success(request, str(s_no) + ' Log in as ' + str(r.auth_role_id))
                    request.session['session_user_id'] = r.auth_id
                    request.session['session_user_lname'] = r.auth_lname
                    request.session['session_user_fname'] = r.auth_fname
                    request.session['session_user_username'] = r.auth_username
                    request.session['session_user_pass'] = r.auth_password
                    request.session['session_user_role'] = f.user_type
                    return HttpResponseRedirect('/home')
                else: 
                    messages.success(request, 'Log in as ' + s_no) # osas staff 
                    request.session['session_user_id'] = r.auth_id
                    request.session['session_user_lname'] = r.auth_lname
                    request.session['session_user_fname'] = r.auth_fname
                    request.session['session_user_username'] = r.auth_username
                    request.session['session_user_pass'] = r.auth_password
                    request.session['session_user_role'] = f.user_type
                    return HttpResponseRedirect('/login')
            else: 
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
                            messages.success(request, str(s_no) + ' is successfully activated!')
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
                messages.error(request, '1111111r' )
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
            messages.success(request, _username + ' ' +  'Successfully Updated!')
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





