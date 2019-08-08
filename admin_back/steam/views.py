from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from ..AdminPackage.AdminController import CheckLogin
from ..AdminPackage.querystring_parser import parser
from .models import Steam,Steam_Data
import json

# Create your views here.

def steam(request):
     checklogin = CheckLogin(request)
     print(checklogin)
     if checklogin == True:

          if request.method == 'POST':
               steam_type = request.POST['type']
               Check_Exist = Steam.objects.filter(steam_name=steam_type)
               if Check_Exist :
                    
                    messages.info(request, "Steam type is already in database please edit it or add another none existing steam type!", extra_tags="warning")
               else:
                    create = Steam.objects.create(steam_name=steam_type, steam_status="Not Configured", steam_link_id = 0)

                    if(create):
                         
                         messages.success(request, "Steam type succesfully added, Please configure it before it can be active.")
              
                    else:
                         messages.error(request, "There was some error please try after sometime.", extra_tags="danger")


                    

          fetch_steam =  Steam.objects.all()
          print(fetch_steam)
          return render(request, 'admin_html/steam.html', {'steam':fetch_steam}) 
     else:
          return redirect('login')


    
    
def CallAction(request, action_name, perform_action_on_id):

     if action_name == 'delete':
          Check_Exist = Steam.objects.filter(id=perform_action_on_id)
          if Check_Exist :

               perform_action = Steam.objects.filter(id=perform_action_on_id).delete()

               if perform_action:
                    messages.success(request, "Steam succesffuly deleted!")

          else:
               messages.error(request, "Steam type does not exist.", extra_tags="danger")


          fetch_steam =  Steam.objects.all()
          print(fetch_steam)
          return render(request, 'admin_html/steam.html', {'steam':fetch_steam})

     if action_name == 'edit':
          
          Check_Exist = Steam.objects.get(id=perform_action_on_id)
          if Check_Exist :

               if request.method == 'POST':
                    get_lvl = {
                         '1':'Single Level',
                         '2':'Double Level',
                         '3':'Triple Level'
                    }
                    level_type = get_lvl[request.POST['level_type']]
                    level = parser.parse(request.POST.urlencode())['level']
                    level = json.dumps(level)


                    obj, insert = Steam_Data.objects.get_or_create(steam_id=perform_action_on_id, steam_data_json=level, multilevel_data=level_type, steam_status="Created")
                    
                    if insert:
                         Check_Exist.steam_status = "Configured"
                         Check_Exist.steam_link_id = obj.id
                    
                         Check_Exist.save()
                         messages.success(request, "Steam succesffuly configured!")
                    
                         
                   # print()
                    #print()

                    

               Check_Exist = Steam.objects.get(id=perform_action_on_id)
               if Check_Exist.steam_status == 'Configured':
                    messages.info(request, "Steam is already configured now it cannot be edited, Delete it and add a new Steam Type")

               return render(request, 'admin_html/steam_edit.html', {'steam':Check_Exist})
               

          else:
               messages.error(request, "Steam type does not exist.", extra_tags="danger")
               return render(request, 'admin_html/steam.html')
          
     if action_name == 'ajax':

          if perform_action_on_id == 1:
                return render(request, 'admin_html/ajax_html/single_steam.html')
          if perform_action_on_id == 2:
                return render(request, 'admin_html/ajax_html/double_steam.html')
          if perform_action_on_id == 3:
                return render(request, 'admin_html/ajax_html/triple_steam.html')

