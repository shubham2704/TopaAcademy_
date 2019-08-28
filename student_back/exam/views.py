from django.shortcuts import render, redirect
from django.http import HttpResponse
from admin_back.admin_main.models import test_data, test_details_advanced, test_details, exam
from admin_back.websettings.models import settings
from django.core.signing import Signer
from admin_back.admin_main.models import exam
from admin_back.test_main.models import question
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, check_account
from ..signup.models import student_academic
from datetime import datetime
from ..view_test_info.models import start_test_details, submited_test_report, start_exam_details, submited_exam_report, exam_realtime_user, exam_realtime_each_question
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser

def realtime_check_cron(request):
    exam_realtime_user.objects.all().delete()
    return HttpResponse(request, "")

def realtime_question(request, exam_session, total, current):
    check_login = login(request)

    if check_login == True:
        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        get_exam = start_exam_details.objects.get(test_session_id=exam_session)

        count_existance = exam_realtime_each_question.objects.filter(test_session_id=get_exam.test_session_id,question_number=current)
        counted=count_existance.count()

        if counted == 0:

            insert = exam_realtime_each_question.objects.create(
                test_session_id=get_exam.test_session_id,
                test_useremail=email,
                question_count=total,
                question_number = current,
                test_started = total,
                test_last_update = timezone.datetime.now(),
                check_ans_number = "",
                TestID = get_exam.TestID,
                ExamID = get_exam.ExamID
            )


    return HttpResponse(request, "")

def realtime_check(request, exam_session):
    check_login = login(request)

    if check_login == True:

        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        get_exam = start_exam_details.objects.get(test_session_id=exam_session)

        count_existance = exam_realtime_user.objects.filter(test_session_id=get_exam.test_session_id)
        counted=count_existance.count()

        if counted == 0:

            insert = exam_realtime_user.objects.create(
                test_session_id=get_exam.test_session_id,
                test_useremail=email,
                ExamID=get_exam.ExamID,
                status = get_exam.TestStatus
            )


    return HttpResponse(request, "")

def exam_started(request, exam_session):
      
    params = {
        "AllowTest" : True,
        "Result" : False,
        "questions": {},
        "test_details": {},
        "timer_end": '',
        "test_data":{},
        "sessionid":exam_session,
        "msg_bool" : False,
        "msg":{}
    }
    check_login = login(request)

    if check_login == True:

        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        get_exam = start_exam_details.objects.get(test_session_id=exam_session)
        get_test = test_details.objects.get(id=get_exam.TestID)
        get_test_adv = test_details_advanced.objects.get(test_id=get_exam.TestID)

        if get_exam.TestStatus == "Submitted":
            get_result = submited_exam_report.objects.get(test_session_id=exam_session)
            params['AllowTest'] = False
            params['Result'] = True
            params['result_data'] = get_result
            params['msg']['msg'] = "Exam is already submited"
            params['msg']['tags'] = "success"
            params['msg']['icon'] = "mdi mdi-timer-off"
            params['msg_bool'] = True
            

        
        if get_exam.resumeable == False  and get_exam.TestStarted == True:
            params['AllowTest'] = False
            params['msg']['msg'] = "Test is Not Resuamable."
            params['msg']['tags'] = "danger"
            params['msg']['icon'] = "mdi mdi-timer-off"
           
            

        if get_test_adv.isAvailDuration == True:
                from_date = get_test_adv.DurationFrom
                today = datetime.today().strftime("%Y-%m-%d %H:%M")
                to_date = get_test_adv.DurationTo
                
                
                if today < from_date:
                    
                    params['AllowTest'] = False
                    params['msg']['msg'] = "This test is not available now it will live on " + str(from_date)
                    params['msg']['tags'] = "warning"
                    params['msg']['icon'] = "mdi mdi-timer-off" 

                #from_time = datetime.fromtimestamp(from_date)
                
                if to_date!='Forever':
                    
                    if today > to_date:
                        params['AllowTest'] = False
                        params['msg']['msg'] = "Exam time is over. You can not attend this Exam now."
                        params['msg']['tags'] = "warning"
                        params['msg']['icon'] = "mdi mdi-timer-off"

        if params['AllowTest'] == True:
            if get_exam.TestStarted == False:
                get_exam.TestStarted = True
                get_exam.save()

            quest_ar = {}
            test_settings = json.loads(get_exam.test_settings)
            i = 0
            for ques in test_settings['question_array']:
                quest_ar[i] = question.objects.get(id=ques)
                i = i + 1
            params['questions'] = quest_ar

            if get_exam.test_istimer == True:

                current_time = timezone.now()
                test_time = get_exam.test_started
                duration = get_exam.timer_duration

                time_diff =  (current_time - test_time).seconds / 60
                params['test_data']['istimer'] = get_exam.test_istimer
                time_left = int(duration) * 60 - time_diff*60
                params['test_data']['time_left'] = time_left

                if time_left < 0:
                    params['test_details'] = get_test
                    params['AllowTest'] = False
                    params['msg']['msg'] = "Time is Over"
                    params['msg']['tags'] = "warning"
                    params['msg']['icon'] = "mdi mdi-timer-off"
                    params['msg_bool'] = True
            #print(params)
            if params['AllowTest'] == True:
                if request.method=="POST":
                    
                    marking = json.loads(get_test.MarkingSetting)
                    buil_dic = {}
                    answers = parser.parse(request.POST.urlencode())['op']
                    ie = 0
                    for ques_ar_count in range(0, i):
                        buil_dic[ques_ar_count] = {}
                        for ques_ar_countt in range(1, 5):
                            if ques_ar_count in answers:
                                if ques_ar_countt in answers[ques_ar_count]:
                                    buil_dic[ques_ar_count][ques_ar_countt] = True
                                else:
                                    buil_dic[ques_ar_count][ques_ar_countt] = False    
                            else:
                                buil_dic[ques_ar_count][ques_ar_countt] = False    
                    and_inc = 0
                    marks_scored = 0
                    correct_ans = 0
                    wrong_ans = 0
                    for key, che_ans in params['questions'].items():
                        sub = buil_dic[and_inc]
                        my1 = sub[1]
                        my2 = sub[2]
                        my3 = sub[3]
                        my4 = sub[4]

                        #print(sub, che_ans.a4)
                        
                        op1 = che_ans.a1
                        op2 = che_ans.a2
                        op3 = che_ans.a3
                        op4 = che_ans.a4
                        correct_count = 0
                        if op1 == True:
                            correct_count = 1 + correct_count

                        if op2 == True:
                            correct_count = 1 + correct_count

                        if op3 == True:
                            correct_count = 1 + correct_count

                        if op4 == True:
                            correct_count = 1 + correct_count

                        
                        if my1 != False:
                            if op1 == my1:
                                marks_scored = marks_scored + float(marking['positive'])/correct_count
                                #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)
                                correct_ans = correct_ans + 1

                            else:
                                marks_scored = marks_scored - float(marking['negative'])/correct_count
                                wrong_ans = wrong_ans + 1
                                #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)

                        if my2 != False:
                                if op2 == my2:
                                    marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        if my3 != False:
                                if op3 == my3:
                                    marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        if my4 != False:
                                if op4 == my4:
                                    marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        and_inc = 1 + and_inc

                    print(buil_dic)
                    count_subm = submited_exam_report.objects.filter(test_session_id=exam_session).count()
                    if  marks_scored >= int(marking['passing']):
                        result="Pass"
                    else:
                        result="Fail"
                    if count_subm == 0:
                        insert = submited_exam_report.objects.create(
                            test_session_id=exam_session,
                            test_useremail=email,
                            test_started=get_exam.test_started,
                            submited_det=json.dumps(buil_dic),
                            scored=marks_scored,
                            total_score=marking['total'],
                            correct=correct_ans,
                            wrong=wrong_ans,
                            clg_rnk="0",
                            class_rnk="0",
                            TestStatus="Submited",
                            ResultStatus=result
                            
                        )

                        if insert:
                            get_exam.TestStatus = "Submitted"
                            get_exam.scored = marks_scored
                            get_exam.save();
                            get_result = submited_exam_report.objects.get(test_session_id=exam_session)
                            params['AllowTest'] = False
                            params['Result'] = True
                            params['result_data'] = get_result
                            params['msg']['msg'] = "Exam is already submited"
                            params['msg']['tags'] = "success"
                            params['msg']['icon'] = "mdi mdi-timer-off"
                            params['msg_bool'] = True
                                    
            
                params['test_details'] = get_test
                params['question_count'] = i - 1

        print(params)

        return render(request, "student_html/exam_start.html", params)




# Create your views here.
def exam_details(request, test_id):
    
    params = {
        "test_button" : True,
        "test_details": {},
        "test_rules": {},
        "messages_er":{}


    }
    check_login = login(request)

    if check_login == True:
        
        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        get_exam = exam.objects.get(id=test_id)
        test_id = get_exam.test_id
        get_user_account = student_academic.objects.get(student_email = email)
        exp_branch = get_user_account.branch.split(":")
        count_qes = question.objects.filter(test_id=test_id).count()
        
        
        
        
        try:

            if request.method == "GET":
                if request.GET['er'] == "015":
                    
                    messages.warning(request, "You have already attended this Test.")

                if request.GET['er'] == "014":
                    
                    messages.warning(request, "Exam is Not Active for your academic year.")

                if request.GET['er'] == "012":
                    
                    messages.warning(request, "Exam time is Over.")
        except:
            pass
            
        try:
            get_test = test_details.objects.get(id=test_id)
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
            params['exam'] = get_exam

            params['get_test_adv'] = get_test_adv
        
            params['test_details']['steam'] = get_test.steam

            params['test_details']['id'] = test_id
            params['test_details']['category_one'] = get_test.category_one
            params['test_details']['category_two'] = get_test.category_two
            params['test_details']['desc'] = get_test.description
            params['test_details']['name'] = get_test.test_name
            params['test_details']['status'] = get_test.status

            if get_test.ask == "All":
                params['test_details']['AskQuestion'] = count_qes
            else:
                params['test_details']['AskQuestion'] = get_test.AskQuestion

            
            params['marking'] = json.loads(get_test.MarkingSetting)

            if get_test.TestType == "Mock":
                params['test_details']['type'] = "Exam"
                params['test_rules'][0] = "Once test started it cannot be stopeed as it is a Mock Test."
                params['test_rules'][1] = "Perofrmance for this test will be saved and comapre with other Students."

            if get_test.TestType == "Practice":
                params['test_details']['type'] = "Exam"
                params['test_rules'][0] = "You can Leave the Test at middle of the test."
                params['test_rules'][1] = "Perofrmance for this test will not be saved."


            if get_test_adv.isTimer == True:
                params['test_details']['timer'] = get_test_adv.TimerLength
                params['test_rules'][2] = "Total time to complte the test is " + str(params['test_details']['timer']) + " min."
                params['test_rules'][3] = "Total " + str(params['test_details']['AskQuestion']) + " will be asked."
            else:
                params['test_details']['timer'] = None
            if get_test.isSCT_test == True:
                if get_test.SCTSteam != exp_branch[0]:
                    params['test_button'] = False
                    params['messages_er']['msg'] = "The uploader has disable the test for your branch and semester."
                    params['messages_er']['tags'] = "info"
                    params['messages_er']['icon'] = "mdi mdi-account-o"

                if get_test.SCTBranch != exp_branch[1]:
                    params['test_button'] = False
                    params['messages_er']['msg'] = "The uploader has disable the test for your branch and semester."  
                    params['messages_er']['tags'] = "info"
                    params['messages_er']['icon'] = "mdi mdi-account-o"
                      
            if get_test_adv.isAvailDuration == True:
                from_date = get_test_adv.DurationFrom
                today = datetime.today().strftime("%Y-%m-%d %H:%M")
                to_date = get_test_adv.DurationTo
                
                
                if today < from_date:
                    
                    params['test_button'] = False
                    params['messages_er']['msg'] = "This test is not available now it will live on " + str(from_date)
                    params['messages_er']['tags'] = "warning"
                    params['messages_er']['icon'] = "mdi mdi-timer-off" 

                #from_time = datetime.fromtimestamp(from_date)
                
                if to_date!='Forever':
                    
                    if today > to_date:
                        params['test_button'] = False
                        params['messages_er']['msg'] = "Exam time is over. You can not attend this Exam now."
                        params['messages_er']['tags'] = "warning"
                        params['messages_er']['icon'] = "mdi mdi-timer-off"
                

        except:
            return redirect("/student/test/browse?status=TestNotFound")

        
        
        
        #print(params)
    print(params)
    return render(request, "student_html/exam_details.html", params)