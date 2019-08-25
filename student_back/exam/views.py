from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
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
from ..view_test_info.models import start_test_details, submited_test_report
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser


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
                        params['messages_er']['msg'] = "This test is not available."
                        params['messages_er']['tags'] = "warning"
                        params['messages_er']['icon'] = "mdi mdi-timer-off"
                

        except:
            return redirect("/student/test/browse?status=TestNotFound")

        
        
        
        #print(params)
    print(params)
    return render(request, "student_html/exam_details.html", params)