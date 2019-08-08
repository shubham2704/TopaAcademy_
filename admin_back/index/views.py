from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.core.signing import Signer
from ..AdminPackage.AdminController import CheckLogin
# Create your views here.

def index(request):
     
     checklogin = CheckLogin(request)
     print(checklogin)

     if checklogin == True:
          return render(request, 'admin_html/index.html') 
     else:
          return redirect('login') 
     
