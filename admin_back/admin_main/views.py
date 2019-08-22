from django.shortcuts import render, HttpResponse,redirect
from ..branch.models import branchs, branch_degree
from ..steam.models import Steam, Steam_Data
from .models import test_details, test_details_advanced
from ..AdminPackage.AdminController import CheckLogin, getUser
from ..AdminPackage.querystring_parser import parser
from django.contrib import messages
from ..websettings.models import settings
import json
from ..Add_Admin.models import users


def conduct_exam(request):

    params = {}
    
    return render(request, "admin_html/exam-conduct.html", params)


def test_action(request):

    params = {}
    
    return render(request, "admin_html/test-action.html", params)


def test_det(request):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}
        get_test = test_details.objects.all()
        params['tests'] = get_test
        return render(request, 'admin_html/test.html', params)





def add_mock_test(request):
    checklogin = CheckLogin(request)

    if checklogin!=True:
        return redirect('/admin-panel/login')

    params = {}
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam
    start_insert = True

    if request.method == "POST":
        test_name = request.POST['test_name']
        test_description = request.POST['test_description']
        test_type = request.POST['test_type']
        isSCT = request.POST.get('isSCT', False) # through exceptional
        category = request.POST['category']
        difficulty = request.POST['difficulty']
        isDate = request.POST.get('isDate', False) # through exceptional
        isTimer = request.POST.get('isTimer', False) # through exceptional
        resume = request.POST.get('resume', False) # through exceptional
        movetopractice = request.POST.get('movetopractice', False) # through exceptional
        shuffle = request.POST.get('shuffle', False) # through exceptional
        sreport = request.POST.get('sreport', False) # through exceptional
        ranking = request.POST.get('ranking', False)
        ask = request.POST['ask']
        ask_number = request.POST['ask_number']
        from_dur = request.POST['from-dur']
        timer_dur = request.POST['timer']
        dur_forever = request.POST.get('dur-forever', False) # through exceptional
        to_dur = request.POST['to-dur']
        email = request.POST.get('email', False)
        sms = request.POST.get('sms', False) # through exceptional
        degree_sct = ''
        branch_sct = ''
        semester_sct = ''
        second_sub_category = ''

        print(request.POST)

        if test_name=='' or test_description=='' or test_type=='' or difficulty=='' or category=='':
            messages.error(request, "All fields are mandatory marked *", extra_tags="danger")
            start_insert = False
        else:

            get_category = Steam.objects.get(steam_link_id=category)
            get_category_data = Steam_Data.objects.get(steam_id=get_category.id)
            category = get_category.steam_name
            category_level = get_category_data.multilevel_data
            print(category_level)
            if category_level =='Single Level':
                sub_category = request.POST['sub_category']
            elif category_level == 'Double Level':
                sub_category = request.POST['sub_category']
                second_sub_category = request.POST['second_sub_category']
                   
            if ranking=='True':
                ranking = True
            if movetopractice=='True':
                movetopractice = True
            if shuffle=='True':
                shuffle = True
            if sreport=='True':
                sreport = True
            
            if resume=='True':
                resume = True
            if isDate=='true':
                isDate = True
                if dur_forever=='True':
                    dur_forever=True 

            if email=='True':
                email = True
            if sms=='True':
                sms = True
            if isTimer=='True':
                isTimer = True

            if isSCT=='on':
                isSCT = True
                degree_sct = request.POST['degree_sct']
                branch_sct = request.POST['branch_sct']
                semester_sct = request.POST['semester_sct']

                if degree_sct=='' or branch_sct=='' or semester_sct=='':
                    messages.error(request, "All fields are mandatory marked *", extra_tags="danger")
                    start_insert = False
                
        if start_insert == True:
            
            add_by = getUser(request).email
            
            obj, insert = test_details.objects.get_or_create(
                test_name= test_name, 
                description=test_description, 
                isSCT_test=isSCT,
                resumeable=resume,
                SCTSteam=degree_sct,
                SCTBranch=branch_sct,
                TestType = test_type,
                SCTSemester=semester_sct,
                TestDifficulty=test_type,
                category_level=category_level,
                steam=category,
                AskQuestion=ask_number,
                sreport=sreport,
                ask=ask,
                ranking = ranking,
                movetopractice = movetopractice,
                shuffle=shuffle,
                category_one=sub_category,
                category_two=second_sub_category,
                category_three="",
                status="Upload QB",
                added_by=add_by
            ) 

            if insert:
                insert_id = obj.id
                if sms == True or email == True:
                    sendnot = 'Yes'
                    to = 'Both'
                if sms == True or email == False:
                    sendnot = 'Yes'
                    to = 'SMS'   
                if sms == False or email ==True:
                    sendnot = 'Yes'
                    to = 'Email'  
                if dur_forever == True:
                    to_dur = "Forever"
                
                insert_adv = test_details_advanced.objects.create(
                    test_id=insert_id,
                    isTimer=isTimer,
                    TimerLength=timer_dur,
                    isAvailDuration=isDate,
                    DurationFrom=from_dur,
                    DurationTo=to_dur,
                    sendNotification=sendnot,
                    NotificationSettings=to

                )  

                if insert_adv:
                    messages.success(request, "Test has been succesfully created now its time to add question bank in the test. <a href='/admin-panel/edit/test/"+ str(insert_id) +"'>Upload Question Bank</a>")    
    


    return render(request, "admin_html/add-mock-test.html", params)

def sct_ajax(request, sct_bool, steam, branch):

    if sct_bool == 'true':
        params = {

            'steam': False,
            'branch':False,
            'type_a':"Semester",
            'semester' : {}

        }
        if steam == 'l':
            branch_deg = branch_degree.objects.all()
            params['get_degree'] = branch_deg
            
            params['steam'] = True
           

            

            
        if branch != 'no':
            params['get_branch'] = branchs.objects.filter(degree_name=branch)
            params['degree_selected'] = branch
            get_degree = branch_degree.objects.get(degree_name=branch)
            sem_list = []
            if get_degree.semester == "Yearly":
                params['type_a'] = "Year"
                
                for rb in range(1 ,int(get_degree.duration) + 1):
                    sem_list.append(rb)
                    
            else:
                for rb in range(1, int(get_degree.semester) + 1):
                    sem_list.append(rb)



            params['branch'] = True
            params['semseter'] = sem_list

            print(params)
        
        
        return render(request, "admin_html/ajax_html/sct.html", params)   
    else:
        return HttpResponse("")

def steam_ajax(request, steam_id):
    params = {}
    params['steam_id']= steam_id

    get_steam_data = Steam_Data.objects.get(id=steam_id)
    get_data = get_steam_data.steam_data_json
    get_level = get_steam_data.multilevel_data
    decode_json = json.loads(get_data)

    if get_level == 'Single Level':
        params['single'] = True
        params['json'] = decode_json
    if get_level == 'Double Level':
        params['multiple'] = True   
        params['json'] = decode_json


    return render(request, "admin_html/ajax_html/steam_addmock.html", params)   

def steam_dual_ajax(request,id, name):
    params = {}
    params['steam_id']= id
    params['dualevel'] = True
    params['name'] = name

    get_steam_data = Steam_Data.objects.get(id=id)
    get_data = get_steam_data.steam_data_json
    get_level = get_steam_data.multilevel_data
    decode_json = json.loads(get_data)
    params['json'] = decode_json

    for looping_steam_data in decode_json:
        val = decode_json[looping_steam_data]['level_name']
        print(val, name)
        
        if val == name:
            print("dss")
            params['dual_data'] = decode_json[looping_steam_data]['data']
        

    print(params['dual_data'])
    return render(request, "admin_html/ajax_html/steam_addmock.html", params)  
    
    