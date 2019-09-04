from admin_back.websettings.models import settings
from django.db.models import Q
import http.client
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
import json
from ..signup.models import student_academic, student_user
from django.db.models import Q
from django.core.signing import Signer


settings = settings.objects.filter(~Q(timezone=''))
email_connect = EmailBackend(host=settings[0].smtp_host, port=settings[0].smtp_port, username=settings[0].smtp_username,use_tls=True, password=settings[0].smtp_password, fail_silently=False)



def send_sms(msg, to, sender_id):
    if settings[0].sms_notification !='' :
        conn = http.client.HTTPSConnection("api.msg91.com")
        headers = {

             'authkey': settings[0].sms_notification,
             'content-type': "application/json"
            }

        array = {
  "sender": "SOCKET",
  "route": "4",
  "country": "91",
  "sender":sender_id,
  "sms": [
    {
      "message": msg,
      "to": [
        to
      ]
    }
  ]
}
        enc_json = json.dumps(array)
        
        conn.request("POST", "/api/v2/sendsms?country=91", enc_json, headers)
        res = conn.getresponse()
        data = res.read()
        
        return data.decode("utf-8")


def login(request):
    
    if 'student_login_session' in request.session:
        print("Logged in")
        return True
            
    else:
        print("Not Logged in")
        return False

def getUser(request, salt):
         
    enc_session = request.session['student_login_session']
    signer = Signer(salt)
    dc = signer.unsign(enc_session)

    params = {}

    params['students'] = student_user.objects.get(email=dc)
    params['academic'] = student_academic.objects.get(student_email=dc)

    return params

def check_account(request, salt):
    
    enc_session = request.session['student_login_session']
    signer = Signer(salt)
    return signer.unsign(enc_session)