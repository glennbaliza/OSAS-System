from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import osas_r_userrole
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'home.html', {})

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {} )

def userrole(request):
    return render(request, 'userrole.html', {})

def adduserrole(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('userrole')
    if request.FILES.get('image'):
        user_pic = request.FILES.get('image')
    else:
        user_pic = 'profile_pic.png'
    try:
        n = osas_r_userrole.objects.get(user_email = email)
        return render(request, 'userrole.html', {
            'error_message': "Duplicated email : " + email
        })
    except ObjectDoesNotExist:
        user_role=osas_r_userrole(user_id=3, user_name=name, user_username=username, user_password=password, user_email=email, user_type=usertype,s_image=user_pic)
        user_role.save()
        return HttpResponseRedirect('/userrole')

