from django.shortcuts import render, HttpResponse
from admin_back.steam.models import Steam, Steam_Data
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.Add_Admin.models import users
import json
from django.http import JsonResponse
# Create your views here.
def browse(request):
    params = {}
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam
    return render(request, "student_html/browse.html", params)

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

    return render(request, "student_html/ajax/steam_addmock.html", params)   

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
    return render(request, "student_html/ajax/steam_addmock.html", params)  
    

def ajax_browse(request):
    
    if request.method == "GET":

        passfull = request.GET['passfull']
        if passfull == 'true':
             get_result = test_details.objects.values_list('id', 'test_name', 'description', 'added_by', 'AskQuestion', 'category_one', 'steam', 'category_two', 'TestType').filter(status='Active')
             count_result = get_result.count()
             print(get_result)
             response_result = {}
             response_result['count'] = count_result
             response_result['data'] = {}
             inc = 0
             for request in get_result:
                 response_result['data'][inc]={}
                 id = request[0]
                 added_by = request[3]
                 get_adv_details = test_details_advanced.objects.values_list('isTimer', 'TimerLength').get(test_id=id)
                 upload_user = users.objects.values_list('first_name', 'lastname').get(email=added_by)
                 response_result['data'][inc]['isTimer'] = get_adv_details[0]
                 response_result['data'][inc]['TimerLength'] = get_adv_details[1]
                 response_result['data'][inc]['added_by'] = upload_user[0] + " " + upload_user[1]
                 response_result['data'][inc]['test_name'] = request[1]
                 response_result['data'][inc]['description'] = request[2]
                 response_result['data'][inc]['AskQuestion'] = request[4]
                 response_result['data'][inc]['id'] = id
                 response_result['data'][inc]['category_one'] = request[5]
                 response_result['data'][inc]['steam'] = request[6]
                 response_result['data'][inc]['test_type'] = request[8]
                 response_result['data'][inc]['category_two'] = request[7]
                 inc = inc+1
        else:
                
             category = request.GET['category']
             subcategory = request.GET['subcategory']
             print(request.GET)
             try:
                 second_category = request.GET['second_category']
             except:
                 second_category = ''


             difficulty = request.GET['difficulty']
             test_type = request.GET['test_type']
             get_category = Steam.objects.get(id=category).steam_name

             build_ar = {}
             build_ar['TestDifficulty'] = difficulty
             build_ar['TestType'] = test_type
             build_ar['status'] = 'Active'
             if category!='All':
                 build_ar['steam'] = get_category
             if subcategory!='All':
                 build_ar['category_one'] = subcategory
             if second_category!='All' and second_category!='':
                 build_ar['category_two'] = second_category

             get_result = test_details.objects.values_list('id', 'test_name', 'description', 'added_by', 'AskQuestion', 'category_one', 'steam', 'category_two', 'TestType').filter(**build_ar)
             count_result = get_result.count()
             print(get_result)
             response_result = {}
             response_result['count'] = count_result
             response_result['data'] = {}
             inc = 0
             for request in get_result:
                 response_result['data'][inc]={}
                 id = request[0]
                 added_by = request[3]
                 get_adv_details = test_details_advanced.objects.values_list('isTimer', 'TimerLength').get(test_id=id)
                 upload_user = users.objects.values_list('first_name', 'lastname').get(email=added_by)
                 response_result['data'][inc]['isTimer'] = get_adv_details[0]
                 response_result['data'][inc]['TimerLength'] = get_adv_details[1]
                 response_result['data'][inc]['added_by'] = upload_user[0] + " " + upload_user[1]
                 response_result['data'][inc]['test_name'] = request[1]
                 response_result['data'][inc]['description'] = request[2]
                 response_result['data'][inc]['AskQuestion'] = request[4]
                 response_result['data'][inc]['id'] = id
                 response_result['data'][inc]['category_one'] = request[5]
                 response_result['data'][inc]['steam'] = request[6]
                 response_result['data'][inc]['test_type'] = request[8]
                 response_result['data'][inc]['category_two'] = request[7]
                 inc = inc+1
        
       # dump_to_json = json.dumps(response_result)
        #print(dump_to_json)

    return JsonResponse(response_result, safe=False)

