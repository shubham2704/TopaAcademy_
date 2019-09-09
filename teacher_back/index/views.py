from django.shortcuts import render, redirect
from ..Controller.all import web_settings, getUser, CheckLogin

# Create your views here.
def index(request):
    if CheckLogin(request) == True:
        params = {}
        params['setting_obj'] = web_settings
        params['teacher'] = getUser(request)


        return render(request, "teacher_html/index.html", params)
    else:
        return redirect("/teacher/login")    
    