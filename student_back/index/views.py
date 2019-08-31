from django.shortcuts import render, HttpResponse
from ..signup.models import student_user, student_academic, student_dashboard_metrices
from ..GlobalModels.main import login, send_sms, email_connect, check_account, settings
from admin_back.admin_main.models import test_data, test_details_advanced, test_details, exam
from admin_back.admin_main.models import exam
from admin_back.branch.models import branchs
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
import os
import json
import string_utils
from django.utils import timezone
from datetime import datetime


def email_verification(request):

    check_login = login(request)
    response_data = {}
    if check_login == True:

        email = check_account(request,settings[0].salt)

        obj = student_user.objects.get(email=email)
        print(settings)
        body = "here is you link to verify you email is <a href='http://" + request.get_host()+ "/student/verify_email/" + obj.email_hash +"'> " + request.get_host()+ "/student/activate/" + obj.email_hash +" </a>"
        sendb = EmailMessage(subject='Verify email - Top Academy', body=body, from_email=settings[0].smtp_email, to=[email],connection=email_connect)
        sendb.content_subtype = "html"
        s = sendb.send()

        if s:
                        
            response_data['status'] = False
            response_data['ntt'] = "success"
            response_data['msg'] = "Verification email sent to " + email

            

    else:

        response_data['status'] = False
        response_data['ntt'] = "error"
        response_data['msg'] = "Invalid action"

    return HttpResponse(json.dumps(response_data), content_type="application/json")            
    


def otp_send(request, number):
    check_login = login(request)
    response_data = {}
    if check_login == True:
        len_number = len(str(number))

        if len_number == 10 :
            
            setting_obj = settings.objects.get(~Q(timezone=''))
            email = check_account(request,setting_obj.salt)
            otp = string_utils.shuffle("54789")
            get_user = student_user.objects.get(email=email)
            get_user.otp = otp
            get_user.phone_no = number
            get_user.save()
        
            msg = "You OTP for phone verification is " + otp
            send = send_sms(msg, number, "RJITAC")
            if send:

                response_data['status'] = True
                response_data['ntt'] = "success"
                response_data['msg'] = "OTP Sent to " + str(number)
        else:
            response_data['status'] = False
            response_data['ntt'] = "warning"
            response_data['msg'] = "Please enter a valid phone number without +91"

    else:

        response_data['status'] = False
        response_data['ntt'] = "error"
        response_data['msg'] = "Invalid action"

    return HttpResponse(json.dumps(response_data), content_type="application/json")            
    
def index(request):

    check_login = login(request)
    pass_args = {"exam":{}}
    branch_array = {}
    get_branch = branchs.objects.all()
    

    #print(get_branch)
    
    for branch in get_branch:

        branch_array.setdefault(branch.degree_name, []).append(branch.branch_name)   

    
    pass_args['branch_array'] = branch_array
    pass_args['branch_array_old'] = get_branch
    #print(branch_array)
    if check_login == True:
       setting_obj = settings
       email = check_account(request,setting_obj[0].salt)
       
       get_user = student_user.objects.get(email=email)
       get_user_aca = student_academic.objects.get(student_id_id=get_user.id)
       
       count= 1 
       if count==1:
           if get_user_aca.branch=='':
               
               pass_args['aca'] = False
               pass_args['branch'] = False
           else:
               pass_args['branch'] = True
               
           if get_user_aca.semester==0:

               pass_args['aca'] = False
               pass_args['semester'] = False
           else:
               pass_args['semester'] = True
           if get_user_aca.profile=='':
               
               pass_args['aca'] = False
               pass_args['profile'] = False
           else:
               pass_args['profile'] = True   
           if get_user_aca.EnrollNo=='':
               
               pass_args['aca'] = False
               pass_args['EnrollNo'] = False
           
           else:
                pass_args['EnrollNo'] = True
       #print(pass_args)
       if get_user.phone_status=='Not Verified':
           pass_args['phone'] = False
           pass_args['aca'] = False
       else:
           pass_args['phone'] = True
       if get_user.email_status=='Not Verified':
           pass_args['email'] = False
       else:
           pass_args['email'] = True    
       if get_user.date_of_birth=='':
           pass_args['dob'] = False    
       else:
           pass_args['dob'] = True
       if request.method == "POST":
           print(request.FILES)
           isProPost = True
          #print( pass_args)
           if pass_args['semester'] == False:
               semesterr = request.POST['semester']
               print(semesterr)
               if semesterr=="0":
                   messages.warning(request, "Please select your current semester.")
               else:
                   get_user_aca.semester = semesterr
                   pass_args['semester'] = True

           if pass_args['EnrollNo'] == False:

                enroll = request.POST['enroll']
                if enroll!='':

                    get_user_aca.EnrollNo = enroll
                    pass_args['EnrollNo'] = True
                    messages.success(request, "Enrollment No. succesfully updated")
                    
                else:
                    messages.warning(request, "Enter your enrollment number.")

           
               

           if pass_args['branch'] == False:
               branch = request.POST['branch']
               
               if branch=='':
                   messages.warning(request, "Please select your branch.")
                   
               else:
                   get_user_aca.branch = branch
                   pass_args['branch'] = True
                   messages.success(request, "Branch succesfully updated")



           if pass_args['profile'] == False:
               
               try:
                   image = request.FILES['avatar']
                   fs = FileSystemStorage()
                   ext = os.path.splitext(image.name)[1]
                   if ext == '.jpg' or ext=='.png':
                       lowercase = str(get_user.id) + get_user.first_name.lower()
                       print(lowercase)
                       upload = fs.save(lowercase+"studentavatar"+ext, image)
                       upload_path = fs.url(upload)
                       if upload:
                           
                           get_user_aca.profile = upload_path
                           pass_args['profile'] = True
                           messages.success(request, "Avatar succesfully uploaded")

                   else:
                       messages.warning(request, "Only jpg and png image is allowed")

                   

               except Exception as e:
                    isProPost = False
                    messages.warning(request, "Please upload a valid image.")
                    print(e)
                    
           if pass_args['dob'] == False:

                dob = request.POST['dob']
                
                if dob=='':
                    messages.warning(request, "Please enter your Date of Birth.")
                    
                else:

                    get_user.date_of_birth = dob
                    pass_args['dob'] = True
                    messages.success(request, "DOB succesfully updated")

                    
           if pass_args['phone'] == False:
               otp = request.POST['otp']
               phone = request.POST['phone']
               

               if phone=='' or otp=='':
                   messages.warning(request, "Please enter the OTP sent to your phone. or request for an another otp")
                   
               else:
                   if phone == get_user.phone_no and otp==get_user.otp:
                       get_user.phone_status = "Verified"
                       pass_args['phone'] = True
                       pass_args['aca'] = True
                       messages.success(request, "Phone succesfully Verified")
                       
                   else:
                       messages.warning(request, "Invalid OTP, Please enter valid OTP")
           get_user.save()
           get_user_aca.save()
       pass_args['user'] = get_user
       sem = get_user_aca.semester
       exp = get_user_aca.branch.split(":")
       if exp[0]!='' and exp[1]!='' and sem!='':
        ie = 0
        get_exam = exam.objects.filter(program=exp[0],branch=exp[1],sem=sem, status='Created')
        today = datetime.today().strftime("%Y-%m-%d %H:%M")
        
        for abss in get_exam:
            exam_det = test_details_advanced.objects.get(test_id=abss.test_id)
            to_date = exam_det.DurationTo

            if today < to_date:

                pass_args['exam'][ie] = abss

        


       
       return render(request, "student_html/index.html", pass_args)
    

