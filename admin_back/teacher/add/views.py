from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connections
from django.core.signing import Signer
from ...AdminPackage.AdminController import CheckLogin
from django.core.signing import Signer
from django.contrib import messages
from .models import add as add_stuff

# Create your views here.

def edit_saff(request, staff_id):
    checklogin = CheckLogin(request)
    

    if checklogin == True:
        params = {"edit":True}
        get_current_saff = add_stuff.objects.filter(id=staff_id)
        select_all = add_stuff.objects.all()
        params['users'] = select_all
        

        if get_current_saff.count() == 1:
            current = add_stuff.objects.get(id=staff_id)
            params['current'] = current

            if request.method=="POST":
                
                f_name = request.POST['first_name']
                prefix = request.POST['prefix']
                lastname = request.POST['lastname']
                employe_id = request.POST['employe_id']
                email = request.POST['email']
                department = request.POST['department']
                designation = request.POST['designation']
                status = request.POST['status']
                phone = request.POST['phone']
                if email!='' and designation!='' and f_name!='' and prefix!='' and lastname!='' and employe_id!='' and department!='' and status!='' and phone!='':
                  current.prefix = prefix
                  current.first_name = f_name
                  current.last_name = lastname
                  current.desination = designation
                  current.department = department
                  current.epployee_id = employe_id
                  current.email = email
                  current.status = status
                  current.phone = phone

                  sd = current.save()

                  if sd is None:
                      messages.success(request, "Staff updated.") 

                 


                else:
                    messages.success(request, "All fields are mandatory", extra_tags="danger")  
                
        

       

        else:
            messages.success(request, "Not Record found.")

        return render(request, "admin_html/teacher_add.html", params)
    else:
        pass

def add(request):
    checklogin = CheckLogin(request)
    

    if checklogin == True:
         params = {}

         select_all = add_stuff.objects.all()
         params['users'] = select_all

         try:
             if request.method=="GET":
                 if request.GET['action'] == "delete":
                     
                     co = add_stuff.objects.filter(id=request.GET['id'])

                     if co.count() == 1:
                         add_stuff.objects.get(id=request.GET['id']).delete()
                         messages.success(request, "Successfully deleted.")
                     else:
                         messages.success(request, "No record found", extra_tags="danger")
         except:
             pass


         if request.method == 'POST':
             f_name = request.POST['first_name']
             prefix = request.POST['prefix']
             lastname = request.POST['lastname']
             employe_id = request.POST['employe_id']
             email = request.POST['email']
             department = request.POST['department']
             designation = request.POST['designation']
             status = request.POST['status']
             phone = request.POST['phone']
             password = request.POST['password']

             if email!='' and designation!='' and f_name!='' and prefix!='' and lastname!='' and employe_id!='' and department!='' and status!='' and phone!='' and password!='':
                 select = True
                 try:
                     check_existence = add.objects.get(email=email)
                     messages.warning(request, "Email is already associal with account")
                     select = False
                 except:
                     select = True

                 if select == True:
                     insert = add_stuff.objects.create(

                         prefix = prefix,
                         first_name = f_name,
                         last_name = lastname,
                         desination = designation,
                         department = department,
                         epployee_id = employe_id,
                         email = email,
                         status = status,
                         phone = phone,
                         password = password


                     )

                     if insert:
                         messages.success(request, "User added")    

             else:
                 messages.warning(request, "All field are mandatory.")

         return render(request, "admin_html/teacher_add.html", params)

    else:
        return redirect('login')
    