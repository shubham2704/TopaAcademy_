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
from .models import start_test_details
import random
import string
import json

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def testing_session(request,test_session_id ):
    pass


# Create your views here.
def startsession(request, test_id):
    
    params = {}
    check_login = login(request)

    if check_login == True:
        #setting_obj = settings.objects.get(~Q(timezone=''))
        #email = check_account(request, setting_obj.salt)
        
        #try:
            get_test = test_details.objects.get(status='Active', id=test_id)
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
            count_prev_test = start_test_details.objects.filter(TestID=test_id).count()
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
                        test_useremail="",
                        test_istimer=get_test_adv.isTimer,
                        timer_duration=get_test_adv.TimerLength,
                        test_settings=json.dumps(test_session_setting),
                        scored="",
                        total_score=int(get_test.AskQuestion) * 10,
                        TestType=get_test.TestType,
                        TestID=test_id,
                        resumeable=True,
                        TestStarted=False

                    )

                    if insert:
                        return redirect("/student/test/session/"+ ses_id)


                    

                    
                else:
                    return redirect("/student/test/browse?status=TestAlreadyDid")


            
            #return redirect("/student/test/session/dasdasd")
            

        #except:
        #    return redirect("/student/test/browse?status=TestNotFound")

 


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