from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from django.db.models import Q
from .models import settings
import os
from ..AdminPackage.AdminController import CheckLogin, getUser, websettings
import json


def settings_call(request):

    checklogin = CheckLogin(request)

    if checklogin == True:
        ab = settings.objects.filter(~Q(timezone=''))
        count_row = ab.count()

        if count_row>0:
            messages.info(request, "Website is already setup, You cannot change the setting please contact your developer.")
            set_obj = settings.objects.get(~Q(timezone=''))

            params = {
                
                'count':count_row,
                'settings':set_obj
                
            
            }
            params['user_login'] = getUser(request)
            params['setting_obj'] = websettings()

            if request.method == 'POST':

                if request.POST['logoo']=='':
                    try:

                        logo = request.FILES['logo']
                        fs = FileSystemStorage()
                        logo_ext = os.path.splitext(logo.name)[1]
                        filename_logo = fs.save("logo"+logo_ext, logo)
                        uploaded_file_url = fs.url(filename_logo)
                        
                        get_s = settings.objects.get(id=ab[0].id)
                        get_s.logo = uploaded_file_url
                        get_s.save()
                        messages.success(request, "Logo succesfully updated")

                    except Exception as e:
                        print(e)
                        messages.info(request, "Select a Image for Logo 250*80px is recommended. Leave if you want to upload favicon only", extra_tags="danger")
                    
                    try:
                         fs = FileSystemStorage()

                         favicon = request.FILES['favicon']
                         fav_ext = os.path.splitext(favicon.name)[1]
                         fav_logo = fs.save("favicon"+fav_ext, favicon)
                         fav_upload = fs.url(fav_logo)
                         
                         get_s = settings.objects.get(id=ab[0].id)
                         get_s.favicon = fav_upload
                         get_s.save()
                         messages.success(request, "Favicon succesfully uploaded")

                    except Exception as e:
                        print(e)
                        messages.info(request, "Select a Image for favicon 64*64 is recommended. Leave if you want to upload Logo only", extra_tags="danger")
                   


        else:
            params = {'count':count_row}
            params['user_login'] = getUser(request)
            params['setting_obj'] = websettings()

            if request.method == 'POST':


                if request.FILES['logo'] and request.FILES['favicon']:
                    website_name = request.POST['website_name']
                    website_des = request.POST['website_des']
                    timezone = request.POST['timezone']
                    salt = request.POST['salt']
                    
                    student = request.POST['student']
                    sms = request.POST['sms']
                    email_allow = request.POST['email']
                    smtp_host = request.POST['smtp_host']
                    port = request.POST['port']
                    smtp_email = request.POST['smtp_email']
                    smtp_username = request.POST['smtp_username']
                    smtp_password = request.POST['smtp_password']

                    
                    if website_des!='' and website_name!='' and timezone!='' and salt!='' and smtp_host!='' and smtp_email!='' and smtp_password!='' and smtp_username!='' and port!='':
                        insert = settings.objects.create(smtp_password=smtp_password, smtp_username=smtp_username, smtp_email=smtp_email,smtp_host=smtp_host,email_notification=email_allow, sms_notification=sms, student_signup=student, logo=uploaded_file_url, favicon=fav_upload, smtp_port=port, website_name=website_name, website_description=website_des, timezone=timezone, salt=salt)
                        if insert:
                            messages.success(request, "Website has been succesfully configured!")
                    else:
                        messages.info(request, "* fields are mandatory.")
            
                else:
                     messages.info(request, "* fields are mandatory.")
        return render(request, 'admin_html/settings.html', params)
    else:
          return redirect('login')