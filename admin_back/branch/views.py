from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.db import connections
from django.core.signing import Signer
from django.db.models import Q
from .models import branch_degree, branchs
import os
from ..AdminPackage.AdminController import CheckLogin
from ..AdminPackage.querystring_parser import parser
import json

def branch(request):

    checklogin = CheckLogin(request)

    if checklogin == True:
        if request.method == 'POST':
            print(request.POST)
            degree = request.POST['degree']
            program = request.POST['program']
            duration = request.POST['duration']
            semseter = request.POST['semseter']

            count = branch_degree.objects.filter(degree_name=degree).count()

            if count==0 and degree!='':

                insert = branch_degree.objects.create(program=program, duration=duration, semester=semseter, degree_name=degree, degree_status='Active')

                if insert:
                    messages.success(request, "Degree has been added")
            else:
                messages.warning(request, "Degree already in database please edit it if needed or invalid degree name.")

        degree_all = branch_degree.objects.all()
        return render(request, "admin_html/branch.html", {'degree_all':degree_all})   
    
    else:
        return redirect("/admin-panel/login") 

def del_degree(request, degree_id):
    
    checklogin = CheckLogin(request)

    if checklogin == True:
        
        count = branch_degree.objects.filter(id=degree_id).count()

        if count==1:

            delete = branch_degree.objects.get(id=degree_id).delete()

            if delete:
                messages.success(request, "Degree has been deleted")
        else:
            messages.warning(request, "Could not find degree")

        degree_all = branch_degree.objects.all()
        return render(request, "admin_html/branch.html", {'degree_all':degree_all})   
    
    else:
        return redirect("/admin-panel/login") 


def edit_degree(request, degree_id):
    
    checklogin = CheckLogin(request)

    if checklogin == True:
        
        count = branch_degree.objects.filter(id=degree_id).count()

        if count==1:
            get_degree = branch_degree.objects.get(id=degree_id)
            
            if request.method == 'POST':
                
                level = parser.parse(request.POST.urlencode())['level']
                count = 0
                insert_b = False
                for lvl in level:
                    name = level[lvl]['name']
                    label = level[lvl]['label']
                    if name is not None:
                        insert = branchs.objects.create(degree_id=degree_id, degree_name=get_degree.degree_name, branch_name=name)
                        if insert:
                            insert_b = True
                            count = 1 + count

                        
                    
                    

                if insert_b == True:
                    messages.success(request,"Branchs succesfully added!")
            branch = branchs.objects.filter(degree_id=degree_id)
            return render(request, "admin_html/branch_edit.html", {'degree':get_degree, 'branchs':branch})

            
        else:
            messages.warning(request, "Could not find degree")
            degree_all = branch_degree.objects.all()
            return render(request, "admin_html/branch.html", {'degree_all':degree_all})
           
    
    else:
        return redirect("/admin-panel/login") 

def del_branch(request, degree_id, branch_id):
    
    checklogin = CheckLogin(request)

    if checklogin == True:
        
        count = branch_degree.objects.filter(id=degree_id).count()
        count_a = branchs.objects.filter(degree_id=degree_id, id=branch_id).count()
        
        if count==1 and count_a==1:

            delete = branchs.objects.get(id=branch_id).delete()

            if delete:
                messages.success(request, "Branch has been deleted")
        else:
            messages.warning(request, "Could not find Branch")

        branch = branchs.objects.filter(degree_id=degree_id)
        degree_all = branch_degree.objects.get(id=degree_id)
        return render(request, "admin_html/branch_edit.html", {'degree':degree_all, 'branchs':branch})  
    
    else:
        return redirect("/admin-panel/login")