from django.db import connections
from django.core.signing import Signer
from ..Add_Admin.models import users
from ..websettings.models import settings
from django.db.models import Q

def CheckLogin(request):

    if 'login_session' in request.session:
        print("Logged in")
        return True
            
    else:
        print("Not Logged in")
        return False
def websettings():
    return settings.objects.get(~Q(timezone=''))
               
def getUser(request):
    setting_obj = settings.objects.get(~Q(timezone=''))
    signer = Signer(setting_obj.salt)
    username = signer.unsign(request.session['login_session'])

    print(username)
    return users.objects.get(email=username)

    
    
