from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.signing import Signer
from django.http import HttpResponse
from django.contrib import messages
from .models import student_user,student_academic, student_dashboard_metrices
from ..GlobalModels.main import  email_connect, send_sms, settings
import string_utils

def activate_account(request, act_hash):
    
    chk = student_user.objects.filter(email_hash=act_hash)

    params = {}

    if chk.count() == 1:
        dc = student_user.objects.get(email_hash=act_hash)
        if dc.email_status == "Not Verified":
            dc.email_status = "Verified"
            dc.save()
            
            params['message'] = "Email is now verified now you can login now."

        else:
            params['message'] = "Email address is already verified, <br>please try to login."
    else:
        params['message'] = "Invalid verification key."
    return render(request, "student_html/activate_email.html", params)    

def signup(request):
    #email = EmailMessage('Subject', 'Body', to=['rs188282@gmail.com'])
    #email.send()

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        password = request.POST['password']
        confirm = request.POST['confirm']
        
        if first_name!='' and last_name!='' and email!='' and phone_no!='' and password!='' and confirm!='':
            if password==confirm:
               
                
                #sms = send_sms("test", "9685925522", "RJITAC")
                #print(sms)

                signer = Signer(settings[0].salt)
                sign_pwd = signer.sign(password)

                check_email =  student_user.objects.filter(email=email).count()
                check_phone =  student_user.objects.filter(phone_no=phone_no).count()
                email_hash = string_utils.shuffle("IHAGFDGJHfhjdfj7863pcdrkjoopkphjkhdsafjhdsfg78367365874")
                otp = string_utils.shuffle("54789")

                if check_email==0 and check_phone==0:
                    obj, insert_user = student_user.objects.get_or_create(first_name=first_name, last_name=last_name, email=email, phone_no=phone_no,password=sign_pwd, account_status='Active', email_hash=email_hash, otp=otp, phone_status='Not Verified', email_status='Not Verified')
                    
                    insert = student_academic.objects.create(student_id_id=obj.id, branch='', semester='0', batch='', profile='/media/avatar.png', subject_preference='', goal='')
                    insert = student_dashboard_metrices.objects.create(student_id_id=obj.id, college_level_rank="0", class_level_rank="0", student_email=email)
                    
                    if insert:
                        msg = "You otp for phone verifiaction is " + otp 
                        body = "here is you link to verify you email is <a href='http://" + request.get_host()+ "/student/verify_email/" + obj.email_hash +"'> " + request.get_host()+ "/student/activate/" + obj.email_hash +" </a>"
                        email = EmailMessage(subject='Verify email - Top Academy', body=body, from_email=settings[0].smtp_email, to=[email],connection=email_connect)
                        email.content_subtype = "html"
                        email.send()
                        send = send_sms(msg, phone_no, "RJITAC")
                        #print(send)
                        messages.success(request, "Your account has been succesfully created please login and verify you email and phone number.")
                
                else:
                    messages.warning(request, "Email or Phone No. is already exist in our record, Please Login")

                #insert = student_user.objects.create()

            else:
                messages.warning(request, "Password doe not match")    
            
        
    return render(request, "student_html/signup.html")
