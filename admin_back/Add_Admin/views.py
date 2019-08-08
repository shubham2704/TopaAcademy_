from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from django.db.models import Q
import os
from ..AdminPackage.AdminController import CheckLogin, getUser
from ..websettings.models import settings
from .models import users
import json


def admin_view(request):

    checklogin = CheckLogin(request)

    if checklogin == True:

        get_all_user = users.objects.all()

        if request.method == 'POST':
            first_name = request.POST['first_name']
            lastname = request.POST['lastname']
            employe_id = request.POST['employe_id']
            department = request.POST['department']
            email = request.POST['email']
            role = request.POST['role']
            phone = request.POST['phone']
            password = request.POST['password']
            status = request.POST['status']

            if status!='' and first_name!='' and lastname!='' and employe_id!='' and department!='' and email!='' and role!='' and phone!='' and password!='':
                
                
                setting_obj = settings.objects.get(~Q(timezone=''))
                salt = setting_obj.salt
                signer = Signer(salt)
                sign_pwd = signer.sign(password) 
                add_by = getUser(request).email
                print(getUser)
               
                insert = users.objects.create(status=status, first_name=first_name, lastname=lastname, employe_id=employe_id, department=department, email=email, role=role, phone_no=phone, password=sign_pwd, added_by_user=add_by)
                if insert:
                    messages.success(request, "User has been succssfully added.")
 
                
            else:
                messages.info(request, "All fields are required")


        return render(request, 'admin_html/admin.html', {'users':get_all_user})


    else:

        return redirect('login')

def admin_edit(request, action, user_id):


    checklogin = CheckLogin(request)

    if checklogin == True:

        get_all_user = users.objects.all()
        if action=='delete' and user_id!='':
            print("Deleteing")
            count = users.objects.filter(id=user_id).count()
            if get_all_user.count()==1:
                messages.warning(request, "There should be two more than two admins to the perform delete action")
                
            else:
                pass
                if count > 0:
                    
                    insert = users.objects.filter(id=user_id).delete()
                    
                    if insert:
                        messages.success(request, "User has been succssfully added.")
                    else:

                        messages.info(request, "User does not exist")
            return render(request, 'admin_html/admin.html', {'users':get_all_user})

        if action=='edit' and user_id!='':
            messages.info(request, "Password can only be changed by getting password reset link on login page.")
            user = users.objects.get(id=user_id)
            
            if request.method == 'POST':

                user.first_name = request.POST['first_name']
                user.lastname = request.POST['lastname']
                user.employe_id = request.POST['employe_id']
                user.department = request.POST['department']
                user.email = request.POST['email']
                user.role = request.POST['role']
                user.phone_no = request.POST['phone']
                user.status = request.POST['status']

                save = user.save()
                
                if save is None:
                    messages.success(request, "Record updated")
            
            
            user = users.objects.get(id=user_id)
            
            return render(request, 'admin_html/admin.html', {'user':user ,'users':get_all_user, 'edit':True})

                

        get_all_user = users.objects.all()
        

    else:
        return redirect('login')