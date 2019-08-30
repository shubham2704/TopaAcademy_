from django.shortcuts import render, HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..branch.models import branchs, branch_degree
from ..steam.models import Steam, Steam_Data
from ..admin_main.models import test_details, test_details_advanced, test_data, exam
from ..AdminPackage.AdminController import CheckLogin, getUser
from ..AdminPackage.querystring_parser import parser
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from student_back.view_test_info.models import start_test_details, submited_test_report, start_exam_details, submited_exam_report, exam_realtime_user, exam_realtime_each_question
from ..websettings.models import settings
from student_back.signup.models import student_user, student_academic
import json
from ..Add_Admin.models import users
import os
import pandas as pd
from datetime import datetime
from django.utils import timezone
# Create your views here.

def user_submission_report(request, exam_session):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {
            'submission': 0,
            'active':0,
            'submission_data':{},
            'active_data':{}
        }

        return render(request, "admin_html/exam-report-session.html")



def monitor_exam_realtime(request, exam_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {
            'submission': 0,
            'active':0,
            'submission_data':{},
            'active_data':{}
        }
        

        count_active = exam_realtime_user.objects.filter(ExamID=exam_id)
        params['active'] = count_active.count()
        count_submission = start_exam_details.objects.filter(TestStatus="Submitted",ExamID=exam_id)
        params['submission'] = count_submission.count()

        i = 0
        for ative_user in count_active:
            active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=ative_user.test_useremail)
            
            json_d = json.loads(active_user.test_settings)
            count_question = len(json_d['question_array'])

            get_currect_question = exam_realtime_each_question.objects.filter(test_session_id=active_user.test_session_id, ExamID=exam_id,test_useremail=ative_user.test_useremail).count()
            get_user_details = student_user.objects.get(email=ative_user.test_useremail)
            get_user_academic = student_academic.objects.get(student_email=ative_user.test_useremail)
            current_time = timezone.now()
            test_time = active_user.test_started
            time_diff =  (current_time - test_time).seconds / 60
            params['active_data'][i] = {
                'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                'Enroll-No': get_user_academic.EnrollNo,
                'Current':get_currect_question,
                'ExamSession':active_user.test_session_id,
                'Total':count_question,
                'Taken':time_diff,
                'Started':test_time.strftime("%d %b, %Y %H:%I %p"),
                'Attendance':active_user.HallAttendence
            }

            i = i + 1
        ii = 0
        for submissions in count_submission:
            active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=submissions.test_useremail)

            submissions_report = submited_exam_report.objects.get(test_session_id=submissions.test_session_id)
            get_user_details = student_user.objects.get(email=submissions.test_useremail)
            get_user_academic = student_academic.objects.get(student_email=submissions.test_useremail)
           
            params['submission_data'][ii] = {
                'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                'Enroll-No': get_user_academic.EnrollNo,
                'Result_Status':submissions_report.ResultStatus,
                'TotalMarks':submissions_report.total_score,
                'ExamSession':active_user.test_session_id,
                'Scored':submissions_report.scored,
                'Started':submissions_report.test_started.strftime("%d %b, %Y %H:%I %p"),
                'Submitted':submissions_report.test_submited.strftime("%d %b, %Y %H:%I %p"),
                'Attendance':submissions.HallAttendence
            }

            ii = ii + 1

        

        

        print(params)
        return JsonResponse(params, safe=False)


def monitor_exam(request, exam_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}
        get_exam = exam.objects.get(id=exam_id)
        get_test_details = test_details.objects.get(id=get_exam.test_id)
        get_test_details_adv = test_details_advanced.objects.get(test_id=get_exam.test_id)

        params['exam_details'] = get_exam
        params['get_test_details'] = get_test_details
        params['get_test_details_adv'] = get_test_details_adv
        print(params)
       
    
    return render(request, "admin_html/monitor-exam.html", params)

def exam_report(request):

    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {
            "submission_data": {}
        }

        all_exam = exam.objects.all()
        params['all_exam']  = all_exam
        
        if request.method=="POST":

            exam_id = request.POST['exam_id']
            

            count_active = exam_realtime_user.objects.filter(ExamID=exam_id)
            params['active'] = count_active.count()
            count_submission = start_exam_details.objects.filter(TestStatus="Submitted",ExamID=exam_id)
            params['submission'] = count_submission.count()

            ii = 0
            for submissions in count_submission:
                active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=submissions.test_useremail)

                submissions_report = submited_exam_report.objects.get(test_session_id=submissions.test_session_id)
                get_user_details = student_user.objects.get(email=submissions.test_useremail)
                get_user_academic = student_academic.objects.get(student_email=submissions.test_useremail)
            
                params['submission_data'][ii] = {
                    'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                    'Enroll-No': get_user_academic.EnrollNo,
                    'Result_Status':submissions_report.ResultStatus,
                    'TotalMarks':submissions_report.total_score,
                    'ExamSession':active_user.test_session_id,
                    'Scored':submissions_report.scored,
                    'Started':submissions_report.test_started.strftime("%d %b, %Y %H:%I %p"),
                    'Submitted':submissions_report.test_submited.strftime("%d %b, %Y %H:%I %p"),
                    'Attendance':submissions.HallAttendence
                }

                ii = ii + 1

            

            

        print(params)
            
    return render(request, "admin_html/exam-report.html", params)