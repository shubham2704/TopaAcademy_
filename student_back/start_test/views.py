from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, check_account

# Create your views here.
def startsession(request, test_id):
    
    params = {}
    check_login = login(request)

    if check_login == True:
        #setting_obj = settings.objects.get(~Q(timezone=''))
        #email = check_account(request, setting_obj.salt)
        get_test = test_details.objects.get(status='Active')
        try:
            get_test_adv = test_details_advanced.objects.get(test_id=test_id)
           

        except:
            return redirect("/student/test/browse?status=TestNotFound")

        
        
        
        
    
    return render(request, "student_html/test_details.html", params)