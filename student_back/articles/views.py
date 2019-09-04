from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, send_sms, email_connect, check_account, settings, getUser
from ..signup.models import student_academic
from admin_back.post.models import content as post_content, attachment as attchm

from datetime import datetime
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser


# Create your views here.

def view_learn(request):
    params = {
            "page": {},
            "pagination": {}

    }
    check_login = login(request)

    if check_login == True:
        setting_obj = settings
        student = getUser(request,setting_obj[0].salt)
        params['student'] = student
        params['setting_obj'] = settings[0]
        email = student['students'].email

        get_sem_det = student_academic.objects.get(student_email=email)
        sem = get_sem_det.semester
        exp = get_sem_det.branch.split(":")

        page_number = 1
        per_page = 20
        build_query = {}

        if request.method=="GET":
                
                try:
                        page_number = int(request.GET['p'])
                        
                        offset = [per_page * page_number, per_page * page_number + per_page]
                        params['page']['number'] = page_number
                        
                except:
                        offset = [0, per_page]
                        
                        
                try:
                        title_q = request.GET['q']
                        params['page']['search'] = True
                except:
                        params['page']['search'] = False

        get_br_post = post_content.objects.filter(status="Published", isSCP=True, SCP_program=exp[0], SCP_branch=exp[1], SCP_semester=sem)
        print(offset)
        params['my'] = {}
        params['my'] = get_br_post
        
        params['page']['number'] = page_number

        if params['page']['search'] == True:
                
                search = post_content.objects.filter((Q(status="Published")) ,
                               (Q(title__icontains=title_q)) |
                               (Q(description__icontains=title_q)) | 
                               (Q(categoryThree__icontains=title_q)) | 
                               (Q(categoryTwo__icontains=title_q)) 
                )

                set_offset = search[offset[0]:offset[1]]
                
                params['page']['result_count'] = search.count()
                params['page']['result_offset_count'] = set_offset.count()
                
                params['page']['search_term'] = title_q
                params['result'] = search
                pag_c = int(float(params['page']['result_count'] / per_page)) + 1
                params['page']['sto'] = offset[0]
                params['page']['page_count_range'] = range(1, pag_c + 1)
                params['page']['page_count'] = pag_c

                

                if pag_c>=10:
                        params['page']['mid_pag'] = int(pag_c - 6)
                        i = 1 
                        for loopnbr in params['page']['page_count_range']:

                                if loopnbr<=5:
                                        params['pagination'][i] = "/student/learning/?p="+ str(loopnbr - 1) +"&q=" + str(title_q)
                                
                                if loopnbr>= pag_c - 5:
                                        params['pagination'][i] = "/student/learning/?p="+ str(loopnbr - 1) +"&q=" + str(title_q)
                                
                                if loopnbr == pag_c - 6:

                                        params['pagination'][i] = ".."
                                i = 1 + i

                                
                                

                else:
                        
                        for loopnbr in params['page']['page_count_range']:
                                
                                params['pagination'][loopnbr] = "/student/learning/?p="+ str(loopnbr - 1) +"&q=" + str(title_q)






                

                

        else:
                search = post_content.objects.filter(status="Published")[offset[0]:offset[1]]
                set_offset = search[offset[0]:offset[1]]
                params['page']['result_count'] = search.count()
                params['page']['result_offset_count'] = set_offset.count()
                params['page']['sto'] = offset[0]
                params['result'] = search
                
                pag_c = int(float(params['page']['result_count'] / per_page)) + 1
                params['page']['page_count'] = pag_c

                params['page']['page_count_range'] = range(1, pag_c + 1)
                if pag_c>=10:
                        params['page']['mid_pag'] = int(pag_c - 6)
                        i = 1 
                        for loopnbr in params['page']['page_count_range']:

                                if loopnbr<=5:
                                        params['pagination'][i] = "/student/learning/?p="+ str(loopnbr - 1)
                                
                                if loopnbr>= pag_c - 5:
                                        params['pagination'][i] = "/student/learning/?p="+ str(loopnbr - 1)
                                
                                if loopnbr == pag_c - 6:

                                        params['pagination'][i] = ".."
                                i = 1 + i

                                
                                

                else:
                        
                        for loopnbr in params['page']['page_count_range']:
                                
                                params['pagination'][loopnbr] = "/student/learning/?p="+ str(loopnbr - 1)





        

        

        print(params)
        return render(request, "student_html/post.html", params)

        

def view_post(request, post_id):

        params = {}

        check_login = login(request)

        if check_login == True:
                setting_obj = settings
                student = getUser(request,setting_obj[0].salt)
                params['student'] = student
                params['setting_obj'] = settings[0]
                email = student['students'].email
                
                try:
                        get_post = post_content.objects.get(id = post_id)
                        params['post']  = get_post
                        attach = attchm.objects.filter(creation_session=get_post.creation_session)
                        params['attachment']  = attach

                        recommand = post_content.objects.filter(
                                (Q(status="Published")) ,
                               (Q(title__icontains=get_post.categoryThree)) |
                               (Q(description__icontains=get_post.categoryThree)) | 
                               (Q(categoryThree__icontains=get_post.categoryThree)) | 
                               (Q(categoryTwo__icontains=get_post.categoryThree))

                        )[0:5]

                        
                        params['recommand']  = recommand


                        

                except Exception as e:
                        print(e)
                        return redirect("/student/learning/")
                
                return render(request, "student_html/view_post.html", params)

