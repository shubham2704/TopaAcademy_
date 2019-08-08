from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.core.signing import Signer
from admin_back.AdminPackage.AdminController import settings
from ..signup.models import student_user
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
             
             try:

                 userss = student_user.objects.get(email=username, password=password, account_status='Active' )
                 print(userss)
                  
                 if userss:

                     login_error = True
                     email = userss.email
                     request.session['student_login_session'] = signer.sign(email)
                     return redirect('../student')
                 else:
                     login_error = False
                     return render(request, 'login.html', {'error_log':login_error}) 
            
             except Exception as e:
                 login_error = False

                 return render(request, 'student_html/login.html', {'error_log':login_error})

                 
            
         else:
             login_error = False
             return render(request, 'student_html/login.html', {'error_log':login_error}) 



    else:
         print(login_error)
         if 'student_login_session' in request.session:
    
             print("Logged in")
             return redirect('../student')  
         else:
             print("Not Logged in")
             return render(request, 'student_html/login.html')          
         