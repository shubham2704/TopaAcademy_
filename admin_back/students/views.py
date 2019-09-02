from django.shortcuts import render, HttpResponse, redirect
from student_back.signup.models import student_user, student_academic, student_dashboard_metrices
from admin_back.websettings.models import settings
from admin_back.branch.models import branchs
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
import os
from ..AdminPackage.AdminController import CheckLogin, getUser, websettings
import json
import string_utils

# Create your views here.
def student_view(request):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
    
        params = {}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
        
        params['students'] = {}

        students = student_user.objects.all()
        i = 0
        for student in students:
            params['students'][i] = {}
            semail = student.email
            academic = student_academic.objects.get(student_email=semail)
            params['students'][i]['name'] = student.first_name + " " + student.last_name
            params['students'][i]['profile'] = str(academic.profile)
            params['students'][i]['branch'] = academic.branch
            params['students'][i]['id'] = student.id
            params['students'][i]['semester'] = academic.semester


            i = 1 + i
            

        print(params)
        return render(request, 'admin_html/students.html', params)


def student_profile_view(request, sid):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:

        params = {}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
        



        return render(request, 'admin_html/students_profile.html', params)