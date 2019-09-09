from admin_back.websettings.models import settings
from admin_back.teacher.add.models import add
from django.core.signing import Signer
from django.db.models import Q

web_settings = settings.objects.get(~Q(timezone=''))

def CheckLogin(request):
    res = False

    if 'teacher_login' in request.session:
        res = True

    return res



def getUser(request):

    if CheckLogin(request) == True:
        
        signer = Signer(web_settings.salt)
        username = signer.unsign(request.session['teacher_login'])
        return add.objects.get(email=username)


   
