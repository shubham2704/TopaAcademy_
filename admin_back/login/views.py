from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.core.signing import Signer
from ..websettings.models import settings
from ..Add_Admin.models import users
from django.db.models import Q

# Create your views here.

def login(request):
    login_error = False
    
    if request.method == "POST":
         username = request.POST['username']
         password = request.POST['password']
         
         login_error = True
         if username!='' and password!='':
             print("Logging in")
             setting_obj = settings.objects.get(~Q(timezone=''))

             signer = Signer(setting_obj.salt)
             password = signer.sign(password)
             #print(users)
             print(password)
             try:

                 userss = users.objects.get(email=username, password=password, status='Active')
                  
                 if userss:
                     
                     login_error = True
                     
                     email = userss.email
                     request.session['login_session'] = signer.sign(email)
                     return redirect('../admin-panel')
                 else:
                     login_error = False
                     return render(request, 'admin_html/login.html', {'error_log':login_error}) 
            
             except Exception as e:
                 login_error = False

                 return render(request, 'admin_html/login.html', {'error_log':login_error})

                 
            
         else:
             login_error = False
             return render(request, 'admin_html/login.html', {'error_log':login_error}) 



    else:
         print(login_error)
         if 'login_session' in request.session:
    
             print("Logged in")
             return redirect('../admin-panel')  
         else:
             print("Not Logged in")
             return render(request, 'admin_html/login.html')          
         
        

