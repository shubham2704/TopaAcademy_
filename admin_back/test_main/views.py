from django.shortcuts import render, HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from ..branch.models import branchs, branch_degree
from ..steam.models import Steam, Steam_Data
from .models import question as qb
from ..admin_main.models import test_details, test_details_advanced, test_data
from ..AdminPackage.AdminController import CheckLogin, getUser, websettings
from ..AdminPackage.querystring_parser import parser
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from ..websettings.models import settings
import json
from ..Add_Admin.models import users
import os
import pandas as pd
from .models import question as qb
from django.http import JsonResponse

def change_status(request, edit_id,bool_s):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {"status":"Success", "msg":"Test Status Changed"}
        

        count_test = test_details.objects.filter(id=edit_id)

        if count_test.count()==1:
            get_test = test_details.objects.get(id=edit_id)

            if get_test.TestType=="Mock":
                if get_test.ranking==True:
                    if get_test.MarkingSetting=='':
                        params['status'] = "Error"
                        params['msg'] = "Update your marking details"

            if get_test.TestType=="Practice":
                if get_test.ranking==True:
                    if get_test.MarkingSetting=='':
                        params['status'] = "Error"
                        params['msg'] = "Update your marking details"


            if get_test.QuestionUploaded == False:
                params['status'] = "Error"
                params['msg'] = "Upload question bank."

            if params['status']=="Success":
                if bool_s == "true":
                    bool_s = "Active"
                else:
                    bool_s = "in Active"    
                
                get_test.status = bool_s
                get_test.save()
        return JsonResponse(params)








def question_bank_view(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {"q_count":0}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    
        if request.method=="GET":
            try:
                if request.GET['action'] == "delete":
                    id_get = request.GET['id']
                    check = qb.objects.filter(id=id_get)
                    if check.count()==1:
                        check.delete()
                        messages.success(request, "Question succesfully deleted")
            except:
                pass
        questions = qb.objects.filter(test_id=edit_id)
        params['questions']= questions
        params['q_count']= questions.count()



        return render(request, "admin_html/qb_view.html", params)




def merge_question_bank(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {"report":False}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

        try:
            get_test = test_details.objects.all()
            params['all_test'] = get_test

          
            print(request.POST)
            if request.method=="POST":
                if 'get_qb' in  request.POST:

                    test_id=request.POST['exam_id']
                    questions = qb.objects.filter(test_id=test_id)
                    params['questions'] = questions
                    print("got_qb")
                    params['report'] = True


                if 'merge' in  request.POST:
                    questions = qb.objects.filter(test_id=edit_id)
                    params['questions'] = questions
                    params['report'] = True
                    got_qb = parser.parse(request.POST.urlencode())['op']
                    merg_inc = 0
                    for key, val in got_qb.items():
                        get_qb = qb.objects.get(id=key)
                        insert = qb.objects.create(
                            test_id=edit_id,
                            question=get_qb.question,
                            explanation=get_qb.explanation,
                            a1=get_qb.a1,
                            a2=get_qb.a2,
                            a3=get_qb.a3,
                            a4=get_qb.a4,
                            o1=get_qb.o1,
                            o2=get_qb.o2,
                            o3=get_qb.o3,
                            o4=get_qb.o4,
                        )
                        if insert:
                            merg_inc = merg_inc + 1


                    messages.success(request, str(merg_inc) + " question were succesfully merged.")


        except Exception as E:
            print(E)

        return render(request, "admin_html/merge_qb.html", params)


def view_question_bank(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    
        

        try:
            get_test = test_details.objects.get(id=edit_id)
            questions = qb.objects.filter(test_id=edit_id)

        
        
        except:
            pass

   

def question_bank(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

        if request.method == "POST":
            question = request.POST['question']
            explain = request.POST['explain']
            q1 = request.POST['a1_a']
            q2 = request.POST['a2_a']
            q3 = request.POST['a3_a']
            q4 = request.POST['a4_a']

            a1 = request.POST.get('a1_c', False)
            a2 = request.POST.get('a2_c', False)
            a3 = request.POST.get('a3_c', False)
            a4 = request.POST.get('a4_c', False)

            if a1 == 'on':
                a1 = True

            if a2 == 'on':
                a2 = True

            if a3 == 'on':
                a3 = True

            if a4 == 'on':
                a4 = True

            b = (a1 == True or a2 == True or a3 == True or a4 == True)
            if question!='' and explain!='' and q1!='' and q2!='' and q3!='' and q4!='' and b == True :
                
                insert = qb.objects.create(

                        test_id = edit_id,
                        question  = question,
                        explanation = explain,
                        a1 = a1,
                        a2 = a2,
                        a3 = a3,
                        a4 = a4,
                        o1 = q1,
                        o2 = q2,
                        o3 = q3,
                        o4 = q4
                )


                if insert:
                    messages.success(request, "Question succesfully added.")

            else:
                messages.warning(request, "All feilds are mandatory and atleasdt one anser should be checjked.", extra_tags="danger")


        check_test = test_details.objects.get(id=edit_id)
        question_count = qb.objects.filter(test_id=edit_id).count()

        if check_test.ask == 'Limited':
            if question_count>=int(check_test.AskQuestion):
                check_test.QuestionUploaded = True
        else:
            if question_count >= 5:
                check_test.QuestionUploaded = True

        check_test.save()
        params['count'] = question_count
        params['test_detail'] = check_test
        return render(request, "admin_html/uqb.html", params)


def edit_test(request, edit_id):
    checklogin = CheckLogin(request)
    if checklogin!=True:
        return redirect('/admin-panel/login')
    else:
        params = {}
        params['user_login'] = getUser(request)
        params['setting_obj'] = websettings()
    

        dirc = {
                            "total":"0",
                            "passing":"0",
                            "positive":"0",
                            "negative":"0"
        }

        try:
            
            get_test = test_details.objects.get(id=edit_id)

            params['test_details'] = get_test
            
            try:
                get_m = json.loads(get_test.MarkingSetting)
                params['marking'] = get_m


            except:
                params['marking'] = dirc

            test_advanced = test_details_advanced.objects.get(test_id=get_test.id)
            params['test_advanced'] = test_advanced
            params['test_data'] = test_data.objects.filter(test_id=get_test.id)

            if request.method == "POST" and request.POST.get('marking_update', False) == '':
                total = request.POST['total']
                passing = request.POST['passing']
                positive = request.POST['positive']
                negative = request.POST['negative']

                if total!='' and passing!='' and positive!='' and negative!='':
                    if int(passing) < int(total):
                        dirc = {
                            "total":total,
                            "passing":passing,
                            "positive":positive,
                            "negative":negative
                        }
                        get_test.MarkingSetting = json.dumps(dirc)

                        get_test.save()

                        messages.success(request, "Marking Setting has been updated")   



                    else:
                        messages.success(request, "Passing marks should be less than Total Marks", extra_tags="danger")    
                        
                else:

                    messages.success(request, "All fields are mandatory", extra_tags="danger") 

               


                


            try:
                if request.method == "POST" and request.POST.get('qb', False) == '':
                
                    
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
        print(params)

    return render(request, "admin_html/test_edit.html", params)

def add_qb_ajax(request, i):
    
    return render(request, "admin_html/ajax_html/add_qb.html", { "i" : i})