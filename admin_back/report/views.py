from django.shortcuts import render, HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ..branch.models import branchs, branch_degree
from ..steam.models import Steam, Steam_Data

from ..admin_main.models import test_details, test_details_advanced, test_data, exam
from ..AdminPackage.AdminController import CheckLogin, getUser, websettings
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

def test_report(request):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {
            "report": False,
            "submission_data": {},
            "topper_data": {}
        }
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()

        all_exam = test_details.objects.all()
        params['all_exam']  = all_exam

        if request.method=="POST":
            params['report'] = True

            exam_id = request.POST['exam_id']

            count_submission = start_test_details.objects.filter(TestStatus="Submitted",TestID=exam_id)
            
            get_exam = test_details.objects.get(id=exam_id)
            
            get_test = test_details.objects.get(id=get_exam.id)
            count_student = student_academic.objects.filter(semester=get_test.SCTSemester, branch=get_test.SCTSteam+":"+get_test.SCTBranch)  
            get_test_adv = test_details_advanced.objects.get(test_id=get_exam.id)
            params['submission'] = count_submission.count()
            params['exam'] = get_exam
            params['test'] = get_test
            params['test_adv'] = get_test_adv
            params['total_students'] = count_student.count()
            params['ratio'] =  round(count_submission.count() / count_student.count() * 100, 2)
            top_scores = submited_test_report.objects.filter(TestID=exam_id).order_by('-scored')[0:5]
            top = 1
            for topper in top_scores:
                active_user = start_test_details.objects.get(TestID=exam_id,test_useremail=topper.test_useremail)
                submissions_report = submited_exam_report.objects.get(test_session_id=topper.test_session_id)
                get_user_details = student_user.objects.get(email=topper.test_useremail)
                get_user_academic = student_academic.objects.get(student_email=topper.test_useremail)

                params['topper_data'][top] = {
                    'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                    'EnrollNo': get_user_academic.EnrollNo,
                    'Result_Status':submissions_report.ResultStatus,
                    'TotalMarks':submissions_report.total_score,
                    'Scored':submissions_report.scored,
                    'per': round(float(submissions_report.scored) / float(submissions_report.total_score) * 100 , 2),
                }

                top = top + 1
            
            

            ii = 0
            for submissions in count_submission:
                active_user = start_test_details.objects.get(TestID=exam_id,test_useremail=submissions.test_useremail)
                submissions_report = submited_test_report.objects.get(test_session_id=submissions.test_session_id)
                get_user_details = student_user.objects.get(email=submissions.test_useremail)
                get_user_academic = student_academic.objects.get(student_email=submissions.test_useremail)
                
                
                params['submission_data'][ii] = {
                    'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                    'EnrollNo': get_user_academic.EnrollNo,
                    'Result_Status':submissions_report.ResultStatus,
                    'TotalMarks':submissions_report.total_score,
                    'per': float(submissions_report.scored) / float(submissions_report.total_score) * 100,
                    'ExamSession':active_user.test_session_id,
                    'Scored':submissions_report.scored,
                    'Started':submissions_report.test_started.strftime("%d %b, %Y %H:%I %p"),
                    'Submitted':submissions_report.test_submited.strftime("%d %b, %Y %H:%I %p"),
                    'wrong':submissions_report.wrong,
                    'correct':submissions_report.correct,
                    'Attendance':submissions.HallAttendence
                }

                ii = ii + 1

            

            

        print(params)


        return render(request, "admin_html/test_report.html", params)




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
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

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
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    
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
            "report": False,
            "submission_data": {},
            "topper_data": {}
        }
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

        all_exam = exam.objects.all()
        params['all_exam']  = all_exam
        
        if request.method=="POST":
            params['report'] = True

            exam_id = request.POST['exam_id']

            count_submission = start_exam_details.objects.filter(TestStatus="Submitted",ExamID=exam_id)
            
            get_exam = exam.objects.get(id=exam_id)
            
            get_test = test_details.objects.get(id=get_exam.test_id)
            count_student = student_academic.objects.filter(semester=get_test.SCTSemester, branch=get_test.SCTSteam+":"+get_test.SCTBranch)  
            get_test_adv = test_details_advanced.objects.get(test_id=get_exam.test_id)
            params['submission'] = count_submission.count()
            params['exam'] = get_exam
            params['test'] = get_test
            params['test_adv'] = get_test_adv
            params['total_students'] = count_student.count()
            params['ratio'] =  round(count_submission.count() / count_student.count() * 100, 2)
            top_scores = submited_exam_report.objects.filter(ExamID=exam_id).order_by('-scored')[0:5]
            top = 1
            for topper in top_scores:
                active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=topper.test_useremail)
                submissions_report = submited_exam_report.objects.get(test_session_id=topper.test_session_id)
                get_user_details = student_user.objects.get(email=topper.test_useremail)
                get_user_academic = student_academic.objects.get(student_email=topper.test_useremail)

                params['topper_data'][top] = {
                    'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                    'EnrollNo': get_user_academic.EnrollNo,
                    'Result_Status':submissions_report.ResultStatus,
                    'TotalMarks':submissions_report.total_score,
                    'Scored':submissions_report.scored,
                    'per': round(float(submissions_report.scored) / float(submissions_report.total_score) * 100 , 2),
                }

                top = top + 1
            
            

            ii = 0
            for submissions in count_submission:
                active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=submissions.test_useremail)
                submissions_report = submited_exam_report.objects.get(test_session_id=submissions.test_session_id)
                get_user_details = student_user.objects.get(email=submissions.test_useremail)
                get_user_academic = student_academic.objects.get(student_email=submissions.test_useremail)
                
                
                params['submission_data'][ii] = {
                    'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                    'EnrollNo': get_user_academic.EnrollNo,
                    'Result_Status':submissions_report.ResultStatus,
                    'TotalMarks':submissions_report.total_score,
                    'per': float(submissions_report.scored) / float(submissions_report.total_score) * 100,
                    'ExamSession':active_user.test_session_id,
                    'Scored':submissions_report.scored,
                    'Started':submissions_report.test_started.strftime("%d %b, %Y %H:%I %p"),
                    'Submitted':submissions_report.test_submited.strftime("%d %b, %Y %H:%I %p"),
                    'wrong':submissions_report.wrong,
                    'correct':submissions_report.correct,
                    'Attendance':submissions.HallAttendence
                }

                ii = ii + 1

            

            

        print(params)
            
    return render(request, "admin_html/exam-report.html", params)



def pdf_exam(request, exam_id):
    
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {
            "report": False,
            "submission_data": {},
            "topper_data": {}
        }
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

        all_exam = exam.objects.all()
        params['all_exam']  = all_exam
        
        

        count_submission = start_exam_details.objects.filter(TestStatus="Submitted",ExamID=exam_id)
        
        get_exam = exam.objects.get(id=exam_id)
        
        get_test = test_details.objects.get(id=get_exam.test_id)
        count_student = student_academic.objects.filter(semester=get_test.SCTSemester, branch=get_test.SCTSteam+":"+get_test.SCTBranch)  
        get_test_adv = test_details_advanced.objects.get(test_id=get_exam.test_id)
        params['submission'] = count_submission.count()
        params['exam'] = get_exam
        params['test'] = get_test
        params['test_adv'] = get_test_adv
        params['total_students'] = count_student.count()
        params['ratio'] = round(count_submission.count() / count_student.count() * 100, 1)
        top_scores = submited_exam_report.objects.filter(ExamID=exam_id).order_by('-scored')[0:5]
        top = 1
        for topper in top_scores:
            active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=topper.test_useremail)
            submissions_report = submited_exam_report.objects.get(test_session_id=topper.test_session_id)
            get_user_details = student_user.objects.get(email=topper.test_useremail)
            get_user_academic = student_academic.objects.get(student_email=topper.test_useremail)

            params['topper_data'][top] = {
                'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                'EnrollNo': get_user_academic.EnrollNo,
                'Result_Status':submissions_report.ResultStatus,
                'TotalMarks':submissions_report.total_score,
                'Scored':submissions_report.scored,
                'per': round(float(submissions_report.scored) / float(submissions_report.total_score) * 100, 1),
            }

            top = top + 1
        
        

        ii = 0
        for submissions in count_submission:
            active_user = start_exam_details.objects.get(ExamID=exam_id,test_useremail=submissions.test_useremail)
            submissions_report = submited_exam_report.objects.get(test_session_id=submissions.test_session_id)
            get_user_details = student_user.objects.get(email=submissions.test_useremail)
            get_user_academic = student_academic.objects.get(student_email=submissions.test_useremail)
            
            
            params['submission_data'][ii] = {
                'FullName':get_user_details.first_name + "" + get_user_details.last_name,
                'EnrollNo': get_user_academic.EnrollNo,
                'Result_Status':submissions_report.ResultStatus,
                'TotalMarks':submissions_report.total_score,
                'per': float(submissions_report.scored) / float(submissions_report.total_score) * 100,
                'ExamSession':active_user.test_session_id,
                'Scored':submissions_report.scored,
                'Started':submissions_report.test_started.strftime("%d %b, %Y %H:%I %p"),
                'Submitted':submissions_report.test_submited.strftime("%d %b, %Y %H:%I %p"),
                'wrong':submissions_report.wrong,
                'correct':submissions_report.correct,
                'Attendance':submissions.HallAttendence
            }

            ii = ii + 1

            

            

        print(params)
            
    return render(request, "admin_html/pdf_report.html", params)

