from django.shortcuts import render, redirect
from admin_back.teacher.add.models import add
from django.contrib import messages
from django.core.signing import Signer
from ..Controller.all import web_settings, getUser, CheckLogin

# Create your views here.

def logout(request):

    try:
        request.session.pop('teacher_login')
        return redirect('/teacher/login')
    except:
        return redirect('/teacher/login')

def login(request):

    if CheckLogin(request) == False:

        if request.method == "POST":
            email = request.POST['username']
            pwd = request.POST['password']
            if email!='' and pwd!='':
                try:
                    signer = Signer(web_settings.salt)
                    get = add.objects.get(email=email, status='Active')
                    getPwd = get.password
                    unsign_pwd = signer.unsign(getPwd)
                    print(unsign_pwd)

                    if pwd == unsign_pwd:
                        request.session['teacher_login'] = signer.sign(get.email)
                        return redirect("/teacher/")

                    else:
                        messages.success(request, "Wrong password or teacher email", extra_tags = "danger")

                except Exception as e:
                    print(e)
                    messages.success(request, "Wrong password or teacher email", extra_tags = "danger")
                
            else:
                messages.success(request, "Enter username and password", extra_tags = "danger")
    else:
        return redirect("/teacher/")
    return render(request, "teacher_html/login.html")