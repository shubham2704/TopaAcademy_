from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from django.db.models import Q
from ..branch.models import branch_degree, branchs
from .models import details
import os
from ..AdminPackage.AdminController import CheckLogin
from ..AdminPackage.querystring_parser import parser
import json
# Create your views here.

def session_view(request):
    param = {
        'session':True,
        'session_from' : '',
        'session_to' : '',
        'data':{}
    }

    checklogin = CheckLogin(request)

    if checklogin == True:
        try:
            check_session = details.objects.get(current_session=True)
            param['session_from'] = check_session.session_from
            param['session_to'] = check_session.session_to

            get_branchs = branch_degree.objects.filter(degree_status="Active")

            for program in get_branchs:

                duration  = program.duration
                degree_name  = program.degree_name
                semseter  = program.semester
                program_id  = program.id
                sem_count = semseter

                if semseter == "Yearly":
                    sem_count = duration

                if semseter == "None":
                    sem_count = 1
                
                sem_count = int(sem_count)

                #for loop in range(sem_count):
                #    print(loop)


        except Exception as e:
            print("No clg session found")
            param['session'] = False
            print(e)

            
        if request.method=="POST" and request.POST['new_session']=='':
            
            try:

                s_from = request.POST['from']
                s_to = request.POST['to']
                
           
                if s_from!='' and s_to!='' and s_to>s_from:
                    insert_session = details.objects.create(
                     current_session=True,
                    session_from=s_from,
                    session_to=s_to,
                    status="Incomplete"
                    )

                    if insert_session:
                         messages.success(request, "Session has been succesfully created")
                         param['session'] = True
                         param['session_from'] = s_from
                         param['session_to'] = s_to
                else:
                    messages.warning(request, "Enter a valid date and duration", extra_tags="warning")
            except Exception as e:
                
                messages.error(request, "Error Occured: " + str(e), extra_tags="danger")
            


    else:
        return redirect("/admin-panel/login")     
    
    return render(request, "admin_html/session_manager.html", param)