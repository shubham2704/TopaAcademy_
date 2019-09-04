from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details, exam
from admin_back.test_main.models import question as ques_model
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, send_sms, email_connect, check_account, settings, getUser
from ..signup.models import student_academic
from datetime import datetime
from .models import start_test_details, submited_test_report, start_exam_details, submited_exam_individual, submited_exam_report
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser

def startsession_exam(request, test_id):
     
    params = {}
    check_login = login(request)
    if  check_login == False:
        return redirect("/student/login")

    if check_login == True:
        setting_obj = settings
        student = getUser(request,setting_obj[0].salt)
        params['student'] = student
        params['setting_obj'] = settings[0]
        email = student['students'].email
        
        
        try:
            get_exam = exam.objects.get(id=test_id)
            
            
            test_id = get_exam.test_id
            get_test = test_details.objects.get(id=test_id)
            mark = json.loads(get_test.MarkingSetting)
            total_mark = mark['total']
            
            if get_test.status !='Active':
                return redirect("/student/exam/details/"+ str(get_exam.id) +"?er=014")

            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
            count_prev_test = start_exam_details.objects.filter(TestID=test_id, ExamID=get_exam.id).exclude(TestStatus="No Completed").count()
            count_question = ques_model.objects.filter(test_id=test_id).count()
            take_exam = True
            ses_id = randomString(10)
            if get_test_adv.isAvailDuration == True:
                start_time = get_test_adv.DurationFrom
                end_time = get_test_adv.DurationTo
                today = datetime.today().strftime("%Y-%m-%d %H:%M")

                if start_time <= today and end_time >= today:
                    take_exam = True
                else:
                    return redirect("/student/exam/details/"+ str(get_exam.id) +"?er=013")
            
             

            if get_test.ask == "All":
                if count_prev_test > 0:
                    return redirect("/student/exam/details/"+ str(get_exam.id) +"?er=015")
                    #Exam already given
                else:
                    test_session_setting = {}
                    test_session_setting['offset'] = "0, "+ str(count_question)
                    test_session_setting['question_array'] = []
                    if get_test.shuffle == True:
                        question = ques_model.objects.filter(test_id=test_id).order_by('?')
                    else:
                        question = ques_model.objects.filter(test_id=test_id)


                    for ques in question:
                        test_session_setting['question_array'].append(ques.id)


            else:
                if count_prev_test * int(get_test.AskQuestion) >= int(get_test.AskQuestion):
                    return redirect("/student/exam/details/"+ str(get_exam.id) +"?er=015")

                else:
                    count_prev_ques = int(count_prev_test) * int(get_test.AskQuestion) # ques asked
                    avg = count_question - count_prev_ques #question left
                    question_offset = str(count_prev_ques) + ", " + str(count_prev_ques + int(get_test.AskQuestion))
                    test_session_setting = {}
                    
                    
                    test_session_setting['offset'] = question_offset
                    test_session_setting['question_array'] = [] 

                    if get_test.shuffle == True:
                        quess = ques_model.objects.filter(test_id=test_id).order_by('?')[count_prev_ques:count_prev_ques + int(get_test.AskQuestion)]
                    else:
                        quess = ques_model.objects.filter(test_id=test_id)[count_prev_ques:count_prev_ques + int(get_test.AskQuestion)]

                    for ques in quess:
                        test_session_setting['question_array'].append(ques.id)

                
            insert = start_exam_details.objects.create(

                        test_session_id=ses_id,
                        test_useremail=email,
                        test_istimer=get_test_adv.isTimer,
                        timer_duration=get_test_adv.TimerLength,
                        test_settings=json.dumps(test_session_setting),
                        scored="",
                        total_score= total_mark,
                        TestType=get_test.TestType,
                        TestID=test_id,
                        ExamID=get_exam.id,
                        resumeable=get_test.resumeable,
                        TestStarted=False

            )
            if insert:
                return redirect("/student/exam/session/"+ str(ses_id))
        except Exception as e:
            print(e)
            return redirect("/student/exam/details/"+ str(get_exam.id) +"?er=015")

 


def randomString(stringLength=10):
    
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def testing_session(request,test_session_id ):
      
    params = {
        "AllowTest" : True,
        "Result" : False,
        "questions": {},
        "test_details": {},
        "timer_end": '',
        "test_data":{},
        "sessionid":test_session_id,
        "msg_bool" : False,
        "msg":{}
    }
    check_login = login(request)
    if  check_login == False:
        return redirect("/student/login")

    if check_login == True:

        setting_obj = settings
        student = getUser(request,setting_obj[0].salt)
        params['student'] = student
        params['setting_obj'] = settings[0]
        email = student['students'].email

        get_exam = start_test_details.objects.get(test_session_id=test_session_id)
        get_test = test_details.objects.get(id=get_exam.TestID)
        get_test_adv = test_details_advanced.objects.get(test_id=get_exam.TestID)

        if get_exam.TestStatus == "Submitted":
            get_result = submited_test_report.objects.get(test_session_id=test_session_id)
            params['AllowTest'] = False
            params['Result'] = True
            params['result_data'] = get_result
            params['msg']['msg'] = "Test is already submited"
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
                quest_ar[i] = ques_model.objects.get(id=ques)
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

                    if get_exam.TestType == "Mock":
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
                                if get_exam.TestType == "Mock":
                                    marks_scored = marks_scored + float(marking['positive'])/correct_count
                                #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)
                                correct_ans = correct_ans + 1

                            else:
                                if get_exam.TestType == "Mock":
                                    marks_scored = marks_scored - float(marking['negative'])/correct_count
                                wrong_ans = wrong_ans + 1
                                #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)

                        if my2 != False:
                                if op2 == my2:
                                    if get_exam.TestType == "Mock":
                                        marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    if get_exam.TestType == "Mock":

                                        marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        if my3 != False:
                                if op3 == my3:
                                    if get_exam.TestType == "Mock":
                                        marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    if get_exam.TestType == "Mock":
                                        marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        if my4 != False:
                                if op4 == my4:
                                    if get_exam.TestType == "Mock":
                                        marks_scored = marks_scored + float(marking['positive'])/correct_count
                                    correct_ans = correct_ans + 1
                                    #print(float(marking['positive'])/correct_count, che_ans.id, correct_count)

                                else:
                                    if get_exam.TestType == "Mock":
                                        marks_scored = marks_scored - float(marking['negative'])/correct_count
                                    wrong_ans = wrong_ans + 1
                                    #print(float(marking['negative'])/correct_count, che_ans.id, correct_count)


                        and_inc = 1 + and_inc

                    print(buil_dic)
                    count_subm = submited_test_report.objects.filter(test_session_id=test_session_id).count()
                    if get_exam.TestType == "Mock":
                        markk = marking['total']
                        if  marks_scored >= int(marking['passing']):
                            result="Pass"
                        else:
                            result="Fail"
                    else:
                        markk = 0
                        result="No Scoring"

                    if count_subm == 0:
                        insert = submited_test_report.objects.create(
                            test_session_id=test_session_id,
                            test_useremail=email,
                            test_started=get_exam.test_started,
                            submited_det=json.dumps(buil_dic),
                            scored=marks_scored,
                            total_score=markk,
                            correct=correct_ans,
                            wrong=wrong_ans,
                            clg_rnk="0",
                            class_rnk="0",
                            TestStatus="Submited",
                            ResultStatus=result,
                            TestID=get_exam.TestID,
                            ExamID="0",
                            
                        )

                        if insert:
                            get_exam.TestStatus = "Submitted"
                            get_exam.scored = marks_scored
                            get_exam.save();
                            get_result = submited_test_report.objects.get(test_session_id=test_session_id)
                            params['AllowTest'] = False
                            params['Result'] = True
                            params['result_data'] = get_result
                            params['msg']['msg'] = "Test is already submited"
                            params['msg']['tags'] = "success"
                            params['msg']['icon'] = "mdi mdi-timer-off"
                            params['msg_bool'] = True
                                    
            
                params['test_details'] = get_test
                params['question_count'] = i - 1

        print(params)

        return render(request, "student_html/test_view.html", params)





# Create your views here.
def startsession(request, test_id):
    
    params = {}
    check_login = login(request)
    if  check_login == False:
        return redirect("/student/login")
    

    if check_login == True:
        setting_obj = settings
        student = getUser(request,setting_obj[0].salt)
        params['student'] = student
        params['setting_obj'] = settings[0]
        email = student['students'].email
        

    
        get_test = test_details.objects.get(id=test_id)
        get_test_adv = test_details_advanced.objects.get(test_id=test_id)
        count_exam = exam.objects.filter(test_id=test_id, status="Created").count()
        #count_prev_test = start_exam_details.objects.filter(TestID=test_id).exclude(TestStatus="No Completed").count()
        count_question = ques_model.objects.filter(test_id=test_id).count()
        
        if count_exam == 0:
            question_ask = get_test.ask
            print(count_exam)
            if question_ask == "All":
                print(question_ask)
                
                count = start_test_details.objects.filter(TestID=test_id).count()
                
                if count == 0:
                    print(count)
                    test_session_setting = {}
                    test_session_setting['offset'] = "0, "+ str(count_question)
                    test_session_setting['question_array'] = []
                    
                    if get_test.shuffle == True:
                        question = ques_model.objects.filter(test_id=test_id).order_by('?')
                    else:
                        question = ques_model.objects.filter(test_id=test_id)


                    for ques in question:
                        test_session_setting['question_array'].append(ques.id)

                    
                else:
                    
                    return redirect("/student/test/details/"+ str(test_id) +"?er=015")  

            elif question_ask == "Limited":
                
                count = start_test_details.objects.filter(TestID=test_id).count()

                asking = int(get_test.AskQuestion)

                ced = count_question - count*asking
                
                if ced >= asking:
                    
                    test_session_setting = {}
                    test_session_setting['offset'] = str(count*asking)+ ", "+ str(count*asking + asking)
                    test_session_setting['question_array'] = []
                    
                    if get_test.shuffle == True:
                        question = ques_model.objects.filter(test_id=test_id).order_by('?')[count*asking:count*asking + asking]
                    else:
                        question = ques_model.objects.filter(test_id=test_id)[count*asking:count*asking + asking]


                    for ques in question:
                        test_session_setting['question_array'].append(ques.id)
                
                else:
                    return redirect("/student/test/details/"+ str(test_id) +"?er=015")  

                
            if get_test.TestType == "Practice":
            
                strr = randomString()
                insert = start_test_details.objects.create(
                    test_session_id = strr,
                    test_useremail = email,
                    test_istimer = get_test_adv.isTimer,
                    timer_duration = get_test_adv.TimerLength,
                    test_settings = json.dumps(test_session_setting),
                    scored = "0",
                    total_score = "0",
                    TestType = get_test.TestType,
                    TestID = test_id,
                    resumeable = get_test.resumeable,
                    TestStarted = False

                )

            if get_test.TestType == "Mock":
                
                strr = randomString()
                if get_test.ranking == True:
                    if get_test.MarkingSetting!='':
                        mark = json.loads(get_test.MarkingSetting)

                    else:
                        return redirect("/student/test/details/"+ str(test_id) +"?er=011")  

                else:
                    return redirect("/student/test/details/"+ str(test_id) +"?er=010")     
                insert = start_test_details.objects.create(
                    test_session_id = strr,
                    test_useremail = email,
                    test_istimer = get_test_adv.isTimer,
                    timer_duration = get_test_adv.TimerLength,
                    test_settings = json.dumps(test_session_setting),
                    scored = "0",
                    total_score = mark['total'],
                    TestType = get_test.TestType,
                    TestID = test_id,
                    resumeable = get_test.resumeable,
                    TestStarted = False

                )
                
            if insert:
                    return redirect("/student/test/session/"+ strr)
            
        else:
            #Under Exam 
            pass
        
            
            

    else:
        return redirect("/student/login")
 


def test_details_view(request, test_id):

    params = {
        "test_button" : True,
        "ask_quesy" : False,
        "test_details": {},
        "test_rules": {},
        "messages_er":{}


    }
    check_login = login(request)
    if  check_login == False:
        return redirect("/student/login")

    if check_login == True:

        setting_obj = settings
        student = getUser(request,setting_obj[0].salt)
        params['student'] = student
        params['setting_obj'] = settings[0]
   
        
        email = student['students'].email

        get_user_account = student_academic.objects.get(student_email = email)
        exp_branch = get_user_account.branch.split(":")
        
        
        try:

            if request.method == "GET":
                if request.GET['er'] == "015":
                    
                    messages.warning(request, "You have already attended this Test.")
                if request.GET['er'] == "010":
                    
                    messages.warning(request, "You cannot attend this test since it is in Exam State")
        except:
            pass
            
        try:
            get_test = test_details.objects.get(id=test_id)
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
            try:
                check_exm = exam.objects.get(test_id=test_id)
                
                get_exam_test = test_details_advanced.objects.get(test_id=check_exm.test_id)
                today = datetime.today().strftime("%Y-%m-%d %H:%M")
                to_date = get_exam_test.DurationTo
                
                if today < to_date:
                    print(check_exm)
                    params['test_button'] = False
                    messages.warning(request, "You cannot attend this test since it is in Exam State")

            except:
                pass
        
            params['test_details']['steam'] = get_test.steam
            params['test_details']['id'] = test_id
            params['test_details']['category_one'] = get_test.category_one
            params['test_details']['category_two'] = get_test.category_two
            params['test_details']['desc'] = get_test.description
            params['test_details']['name'] = get_test.test_name
            params['test_details']['status'] = get_test.status
            if get_test.AskQuestion!='':
                params['ask_quesy'] = True
            params['test_details']['AskQuestion'] = get_test.AskQuestion

            if get_test.TestType == "Mock":
                params['test_details']['type'] = "Mock Test"
                params['test_rules'][0] = "Once test started it cannot be stopeed as it is a Mock Test."
                params['test_rules'][1] = "Perofrmance for this test will be saved and comapre with other Students."

            if get_test.TestType == "Practice":
                params['test_details']['type'] = "Practice Test"
                params['test_rules'][0] = "You can Leave the Test at middle of the test."
                params['test_rules'][1] = "Perofrmance for this test will not be saved."


            if get_test_adv.isTimer == True:
                params['test_details']['timer'] = get_test_adv.TimerLength
                params['test_rules'][2] = "Total time to complte the test is " + str(params['test_details']['timer']) + " min."
                params['test_rules'][3] = "Total " + str(get_test.AskQuestion) + "will be asked."
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
                today = datetime.today().strftime("%Y-%m-%d")
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
                        params['messages_er']['msg'] = "This test is not available."
                        params['messages_er']['tags'] = "warning"
                        params['messages_er']['icon'] = "mdi mdi-timer-off" 
                

        except:
            return redirect("/student/test/browse?status=TestNotFound")

        
        
        
        #print(params)
    
    return render(request, "student_html/test_details.html", params)