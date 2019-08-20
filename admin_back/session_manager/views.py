from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from django.db.models import Q
from ..branch.models import branch_degree, branchs
from .models import data as ses_dat, data_semseter, details
import os
from ..AdminPackage.AdminController import CheckLogin
from ..AdminPackage.querystring_parser import parser
from ..teacher.add.models import add as staff
import json
# Create your views here.



def session_ajax_modal_view(request, id):

    checklogin = CheckLogin(request)
    param = {}

    if checklogin == True:
        try:

            check_ses_data_id = data_semseter.objects.get(id = id)
            get_all_staff = staff.objects.all()
            param['current_det'] =  check_ses_data_id
            param['all_staff'] = get_all_staff
            
        except:
            pass
        print(check_ses_data_id)
     

    else:
        pass 

    
    return render(request, "admin_html/ajax_html/session_manage_modal.html", param)

def session_view(request):
    param = {
        'session':True,
        'Teaching':{},
        'TimeTable':{},
        'AcademyCalender':{},
        'session_from' : '',
        'session_to' : '',
        'session_id' : '',
        'data':{}
    }

    

    checklogin = CheckLogin(request)

    if checklogin == True:
        try:
            check_session = details.objects.get(current_session=True)
            param['session_from'] = check_session.session_from
            param['session_to'] = check_session.session_to
            param['session_id'] = check_session.id

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
                
        get_all_branch = branchs.objects.all()

        for branchGot in get_all_branch:
            
            branch_degree_detail = branch_degree.objects.get(id=branchGot.degree_id)
            br_name = branchGot.branch_name
            dr_name = branchGot.degree_name
            duration = branch_degree_detail.duration
            sem = branch_degree_detail.semester
            

            try:
                check_man_data = ses_dat.objects.get(program=dr_name, branch=br_name)
                print("sd", br_name)
           
            except:
                insert_get, insert = ses_dat.objects.get_or_create(
                data_status=False, 
                program=dr_name,
                option_txt="NO DATA",
                branch=br_name,
                session_id=check_session
                )
                
                sem_list = {}
                list_inc = 0
                if sem == "Yearly":
                
                    for rb in range(1 ,int(duration) + 1):

                        sem_ins, sem_ins_st = data_semseter.objects.get_or_create(
                            data_status=False, 
                            duration_type=branch_degree_detail.duration+"|"+sem,
                            duration_number=rb,
                            ClassTeacher_ID="",
                            HOD_ID="",
                            data_id=insert_get,
                            session_id=check_session
                            )


                        sem_list[list_inc] = {}
                        sem_list[list_inc]['dataa'] = {}
                        sem_list[list_inc]['TeachingSatatus'] = False
                        sem_list[list_inc]['TimeTable'] = False
                        sem_list[list_inc]['dataa'][rb] = {}
                        #sem_list[list_inc]['dataa'][rb]['sem_data_id'] = sem_ins['id']
                        sem_list[list_inc]['dataa'][rb]['status'] = False


                        list_inc = 1 + list_inc
                else:

                    for rb in range(1, int(sem) + 1):
                        
                        sem_ins, sem_ins_st = data_semseter.objects.get_or_create(
                            data_status=False, 
                            duration_type=branch_degree_detail.duration+"|"+sem,
                            duration_number=rb,
                            ClassTeacher_ID="",
                            HOD_ID="",
                            data_id=insert_get,
                            session_id=check_session
                            )


                        sem_list[list_inc] = {}
                        sem_list[list_inc]['dataa'] = {}
                        sem_list[list_inc]['TeachingSatatus'] = False
                        sem_list[list_inc]['TimeTable'] = False
                        sem_list[list_inc]['dataa'][rb] = {}
                        #sem_list[list_inc]['dataa'][rb]['sem_data_id'] = sem_ins['id']
                        sem_list[list_inc]['dataa'][rb]['status'] = False



                        list_inc = 1 + list_inc
   
    else:
        return redirect("/admin-panel/login")  


    get_session_sem = ses_dat.objects.all()
    idv_inc = 0
    for indv_dt in get_session_sem:
        param['data'][idv_inc] = {}
        param['data'][idv_inc]['program'] = indv_dt.program
        param['data'][idv_inc]['branch'] = indv_dt.branch
        param['data'][idv_inc]['data'] = {}
        dhg = data_semseter.objects.filter(session_id = param['session_id'], data_id = indv_dt.id)
        param['data'][idv_inc]['data'] = dhg

        idv_inc = idv_inc + 1


    print(param)
    
    return render(request, "admin_html/session_manager.html", param)