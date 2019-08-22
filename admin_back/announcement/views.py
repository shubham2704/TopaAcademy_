from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.core.signing import Signer
from ..AdminPackage.AdminController import CheckLogin
from ..teacher.add.models import add as staff
from student_back.signup.models import student_user
from ..session_manager.models import details as session_mdetails, data_semseter, data as session_data

# Create your views here.

def announcement_view(request):

    params = {}
    params['hod'] = {}
    params['classteacher'] = {}
    checklogin = CheckLogin(request)
   
    if checklogin == True:

        get_all_staff = staff.objects.all()
        get_all_students = student_user.objects.all()
        params['staff'] = get_all_staff
        params['students'] = get_all_students
      
        get_active_session = session_mdetails.objects.get(current_session=True)
        get_all_session_sem = data_semseter.objects.filter(session_id = get_active_session, data_status = True)
        print(params['hod'].keys)
        for app_fliter in get_all_session_sem:
            hod = str(app_fliter.HOD_ID)
            class_teacher = str(app_fliter.ClassTeacher_ID)
            if hod not in params['hod']:
                params['hod'][hod] = {}
                idd = int(app_fliter.HOD_ID)
                
                params['hod'][hod] = staff.objects.get(id = idd)

                

            if class_teacher not in params['classteacher']:
                params['classteacher'][class_teacher] = {}
                idd = int(class_teacher)
                params['classteacher'][class_teacher] = staff.objects.get(id = idd)
           




        print(params)
        return render(request, "admin_html/announcement.html", params)
