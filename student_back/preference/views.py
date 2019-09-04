from django.shortcuts import render, redirect
from admin_back.steam.models import Steam, Steam_Data
import json
from admin_back.AdminPackage.querystring_parser import parser

from ..GlobalModels.main import login, send_sms, email_connect, check_account, settings, getUser
from django.contrib import messages
from django.db.models import Q
from django.core.signing import Signer
from ..signup.models import student_academic


def preference(request):

    check_login = login(request)
    if  check_login == False:
        return redirect("/student/login")
    param = {}
    if login(request) == True:
        setting_obj = settings
        #print()
        student = getUser(request,setting_obj[0].salt)
        param['student'] = student
        param['setting_obj'] = settings[0]
        email = student['students'].email
        
        
    else:
        return redirect("/student/login")
    
    get_steam = Steam.objects.all()
    get_academic = student_academic.objects.get(student_email=email)
    
    if request.method == "POST":
        try:
             item = parser.parse(request.POST.urlencode())['team']
             get_academic.subject_preference = json.dumps(item)
             insert = get_academic.save()
             print(insert)
             if ins is None:
                 messages.error(request, "Preferrence has been succesfully set.")
        except:
            messages.error(request, "Please select atleast one topic.")
    
    i = 0
    
    param['steam_d'] = {}
    for steam in get_steam:
        param['steam_d'][i] = {}
        steam_id = steam.id
        param['steam_d'][i]['steam_name'] = steam.steam_name
        da = Steam_Data.objects.get(steam_id=steam_id)
        param['steam_d'][i]['steam_data'] =  da
        load_json = json.loads(da.steam_data_json)
        param['steam_d'][i]['json'] = load_json
        
        i = i+1
    
    param['mypref'] = {}
    mypref = json.loads(get_academic.subject_preference)
    exp_inc = 0
    for exp in mypref['item']:
        param['mypref'][exp_inc] = {}
        explode = exp.split(":")
        param['mypref'][exp_inc] = explode
        exp_inc = exp_inc + 1
        
    return render(request, "student_html/preference.html", param)