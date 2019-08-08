from django.shortcuts import render, HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from ..branch.models import branchs, branch_degree
from ..steam.models import Steam, Steam_Data
from ..admin_main.models import test_details, test_details_advanced, test_data
from ..AdminPackage.AdminController import CheckLogin, getUser
from ..AdminPackage.querystring_parser import parser
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from ..websettings.models import settings
import json
from ..Add_Admin.models import users
import os
import pandas as pd

# Create your views here.
def edit_test(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}

        try:
            
            get_test = test_details.objects.get(id=edit_id)
            params['test_detail'] = get_test
            test_advanced = test_details_advanced.objects.get(test_id=get_test.id)
            params['test_advanced'] = test_advanced
            params['test_data'] = test_data.objects.filter(test_id=get_test.id)
            if request.method == "POST" and request.POST['qb'] == '':
               
                try:
                    file = request.FILES['file-2']
                    file_extension = os.path.splitext(file.name)[1]
                    fs = FileSystemStorage()
                    upload = fs.save("fasde"+file_extension, file)
                    upload_path = fs.url(upload)
                    load_file = pd.read_csv("http://127.0.0.1:8000" + str(upload_path))
                    if file_extension == '.csv' or file_extension=='.xlsx':
                        if file_extension == '.csv':
                            load_file = pd.read_csv("http://127.0.0.1:8000" + str(upload_path))
                        if file_extension == '.xlsx':
                           load_file = pd.read_excel("http://127.0.0.1:8000" + upload_path, sheetname=0)
                        #print(load_file)
                        count_insert = 0
                        for index, row in load_file.iterrows():
                             question = row[0]
                             op1 = row[1]
                             op2 = row[2]
                             op3 = row[3]
                             op4 = row[4]
                             ans = row[5]
                             insert = test_data.objects.create(

                                 test_id= edit_id,
                                 question=question,
                                 optionOne=op1,
                                 optionTwo=op2,
                                 optionThree=op3,
                                 optionFour = op4, 
                                 answer=ans



                             )

                             if insert:
                                 count_insert = count_insert+1
                        if count_insert>0:
                            messages.success(request, "Question Bank succesfully uplloaded, Total Questions : " +  str(count_insert))
                            get_test.status = "Active"
                            get_test.save()

                    else:
                        messages.info(request, "Upload only CSV or XLSX file.")

                except Exception as e:
                     
                     if str(e) == "'file-2'":
                         messages.error(request, "Error Occured : Please Upload a vaild file .csv or .xlxs" , extra_tags="danger")
                         
                     else:
                         messages.error(request, "Error Occured : " + str(e), extra_tags="danger")
                
                    
                
        except ObjectDoesNotExist:
            return redirect('/admin-panel/test/?ac=not-exist')

       
            

        params['tests'] = get_test

    return render(request, "admin_html/test_edit.html", params)

def add_qb_ajax(request, i):
    
    return render(request, "admin_html/ajax_html/add_qb.html", { "i" : i})