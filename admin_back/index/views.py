from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.contrib import messages
from django.core.signing import Signer
from ..websettings.models import settings
from ..AdminPackage.AdminController import CheckLogin, getUser, websettings
# Create your views here.

def index(request):
     
     checklogin = CheckLogin(request)
     
     

     if checklogin == True:
          params = {}
          params['user_login'] = getUser(request)
          params['setting_obj'] = websettings()
          print(params['user_login'].first_name)
          
          
          
          return render(request, 'admin_html/index.html', params)

     else:
          return redirect('/admin_html/login') 
     
