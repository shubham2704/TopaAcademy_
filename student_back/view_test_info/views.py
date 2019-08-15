from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, check_account
from ..signup.models import student_academic
from datetime import datetime
from .models import start_test_details, submited_test_report
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser

def randomString(stringLength=10):
    
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def testing_session(request,test_session_id ):
    params = {

        "testView":True,
        "result":{},
        "resumeable":True,
        "complete":False,
        "st":"",
        "icon":"",
        "st_title":"",
        "msg_msg":"",
        "msg_d":False,
        "test_data": {
            "questions_counts":0
        }

    }
    check_login = login(request)

    if check_login == True:
        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        get_test_stated_session = start_test_details.objects.get(test_session_id=test_session_id, test_useremail=email)
        istim = get_test_stated_session.test_istimer
        test_det = test_details.objects.get(id=get_test_stated_session.TestID)
        params['resumeable'] = get_test_stated_session.resumeable
        params['test_details'] = test_det
        
        if get_test_stated_session.TestStatus == "No Completed":

            params['testView'] = False
            params['st'] = "info"
            params['st_title'] = "Session Removed"
            params['icon'] = "mdi mdi-delete"
            params['msg_d'] = True
            get_test_stated_session.TestStatus = "No Completed"
            params['msg_msg'] = "The test session is removed possible reasons may be Test Time Limit exceed, Resumablimity is Disabled by Uploader or Test not submited for long time."


        
        if get_test_stated_session.TestStatus == "Started":

        
            if istim == True:
                current_time = timezone.now()
                test_time = get_test_stated_session.test_started
                duration = get_test_stated_session.timer_duration
                time_diff =  (current_time - test_time).seconds / 60

                if time_diff > int(duration):
                    params['testView'] = False
                    params['st'] = "warning"
                    params['st_title'] = "Test Time Limit Exceeded"
                    params['icon'] = "mdi mdi-timer-off"
                    params['msg_d'] = True
                    get_test_stated_session.TestStatus = "No Completed"
                    params['msg_msg'] = "Sorry test times is expired, You cannot resume the test please start the test from begininmg (if avail)."

        
            if get_test_stated_session.resumeable == False and get_test_stated_session.TestStarted == True:
                
                    params['testView'] = False
                    params['st'] = "warning"
                    params['icon'] = "mdi mdi-close-circle-o"
                    params['msg_d'] = True
                    params['st_title'] = "Cannot Resume the Test"
                    params['msg_msg'] = "Sorry test the test cannot be resumed, Please test please start from begininmg(if avail)."
                    get_test_stated_session.TestStatus = "No Completed"

        if get_test_stated_session.TestStatus == "Completed":
            params['testView'] = False
            params['complete'] = True
            check = submited_test_report.objects.get(test_session_id = test_session_id)
            params['result']['class_rank'] = check.class_rnk
            params['result']['clg_rank'] = check.clg_rnk
            params['result']['pts'] = check.scored
            params['result']['total_pts'] = check.total_score
            params['complete'] = True
            params['result']['msg_body'] = "You scorred " + str(check.scored) + " pts out of "  + str(check.total_score) + " pts and " + str(check.correct) + " were correct and rest incorrect."
            

        #print(params) 

        if params['testView'] == True:
            get_test_stated_session.TestStarted = True
            if istim == True:
                params['test_data']['istimer'] = istim
                time_left = int(duration) * 60 - time_diff*60
                params['test_data']['time_left'] = time_left
            load_test_setting = json.loads(get_test_stated_session.test_settings)

            offset = load_test_setting['offset'].split(", ")
            get_questions = test_data.objects.filter(test_id=get_test_stated_session.TestID)[int(offset[0]):int(offset[1])]
            count = get_questions.count()
            lst_of_qs = {}
            i = 1
            for rn in get_questions:
                lst_of_qs[i] = rn

                i = 1+i

            params['test_data']['questions_count'] = lst_of_qs
            params['test_data']['questions_counts'] = count
           
                
                #print( params)

        if request.method == "POST" and request.POST['submit_test']=='':
            
            answers = parser.parse(request.POST.urlencode())['ans']

            if len(answers) == params['test_data']['questions_counts']:
                answers_json = json.dumps(answers)
                pts_total = get_test_stated_session.total_score
                pts_scored = 0
                correct_answ = 0
                wrong_ans = 0
                pts_avg = int(pts_total) / params['test_data']['questions_counts']
                for key, val in answers.items():
                    get_ansforq = test_data.objects.get(id=key)

                    if get_ansforq.answer == val:

                        correct_answ = 1 + correct_answ
                        pts_scored = pts_avg + pts_scored

                    else:
                        wrong_ans = 1 + wrong_ans

                if get_test_stated_session.TestType == "Mock":
                    get_test_stated_session.scored = pts_scored
                    


                if get_test_stated_session.TestType == "Practice":
                    get_test_stated_session.scored = 0
                    
                try:
                    
                    check = submited_test_report.objects.get(test_session_id = test_session_id)
                    params['result']['class_rank'] = check.class_rnk
                    params['result']['clg_rank'] = check.clg_rnk
                    params['result']['pts'] = check.scored
                    params['result']['total_pts'] = check.total_score
                    params['complete'] = True
                    params['result']['msg_body'] = "You scorred " + str(check.scored) + "pts out of "  + str(check.total_score) + " pts and " + str(check.correct) + "were correct and rest incorrect."
                    

                except:
                    

                    params['result']['class_rank'] = 10
                    params['result']['clg_rank'] = 21
                    params['result']['pts'] = pts_scored
                    params['result']['total_pts'] = pts_total
                    params['result']['msg_body'] = "You scorred " + str(pts_scored) + " pts out of "  + str(pts_total) + " pts and " + str(correct_answ) + " were correct and rest incorrect."
                    
                   

                    insert = submited_test_report.objects.create(
                        test_session_id = test_session_id,
                        test_useremail = email,
                        test_started = get_test_stated_session.test_started,
                        submited_det = answers_json,
                        scored = pts_scored,
                        total_score = pts_total,
                        correct = correct_answ,
                        wrong = wrong_ans,
                        clg_rnk = params['result']['clg_rank'],
                        class_rnk = params['result']['class_rank'],
                        TestStatus = "Submited", 
                    )

                    if insert:
                        get_test_stated_session.TestStatus = "Completed"
                        params['complete'] = True
                        params['testView'] = True

                




               

                
            else:
                messages.warning(request, "Make sure to give anwers to all queston.")

        get_test_stated_session.save()
        params['sessionid'] = test_session_id
        params['TestID'] = get_test_stated_session.TestID
        print(params)
        return render(request, "student_html/test_view.html", params)

        



# Create your views here.
def startsession(request, test_id):
    
    params = {}
    check_login = login(request)

    if check_login == True:
        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)
        
        try:
            get_test = test_details.objects.get(status='Active', id=test_id)
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
            count_prev_test = start_test_details.objects.filter(TestID=test_id).exclude(TestStatus="No Completed").count()
            count_question = test_data.objects.filter(test_id=test_id).count()

            if get_test.TestType == "Mock":
                count_prev_ques = int(count_prev_test) * int(get_test.AskQuestion) # ques asked
                avg = count_question - count_prev_ques #question left

                print(count_question, count_prev_ques, avg, int(get_test.AskQuestion))

                if  avg >= int(get_test.AskQuestion):

                    question_offset = str(count_prev_ques) + ", " + str(count_prev_ques + int(get_test.AskQuestion))
                    test_session_setting = {}
                    test_session_setting['offset'] = question_offset
                    ses_id = randomString(10)

                    insert = start_test_details.objects.create(

                        test_session_id=ses_id,
                        test_useremail=email,
                        test_istimer=get_test_adv.isTimer,
                        timer_duration=get_test_adv.TimerLength,
                        test_settings=json.dumps(test_session_setting),
                        scored="",
                        total_score=int(get_test.AskQuestion) * 10,
                        TestType=get_test.TestType,
                        TestID=test_id,
                        resumeable=get_test.resumeable,
                        TestStarted=False

                    )

                    if insert:
                        return redirect("/student/test/session/"+ ses_id)


                    

                    
                else:
                    #messages.info(request, "You have already gave to all tests of this test.")
                    return redirect("/student/test/details/"+ str(test_id) +"?er=015")
                    


            
            #return redirect("/student/test/session/dasdasd")
            

        except:
            return redirect("/student/test/details/"+ str(test_id) +"?er=015")

 


def test_details_view(request, test_id):

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

        get_user_account = student_academic.objects.get(student_email = email)
        exp_branch = get_user_account.branch.split(":")
        
        

        if request.method == "GET":
            if request.GET['er'] == "015":
                
                messages.warning(request, "You have already attended this Test.")

        try:
            get_test = test_details.objects.get(id=test_id)
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
        
            params['test_details']['steam'] = get_test.steam
            params['test_details']['id'] = test_id
            params['test_details']['category_one'] = get_test.category_one
            params['test_details']['category_two'] = get_test.category_two
            params['test_details']['desc'] = get_test.description
            params['test_details']['name'] = get_test.test_name
            params['test_details']['status'] = get_test.status
            params['test_details']['AskQuestion'] = get_test.AskQuestion

            if get_test.TestType == "Mock":
                params['test_details']['type'] = "Mock Test"
                params['test_rules'][0] = "Once test started it cannot be stopeed as it is a Mock Test."
                params['test_rules'][1] = "Perofrmance for this test will be saved and comapre with other Students."

            if get_test.TestType == "Practice":
                params['test_details']['type'] = "Mock Test"
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