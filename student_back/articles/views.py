from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, check_account
from ..signup.models import student_academic
from admin_back.post.models import content as post_content
from datetime import datetime
import random
import string
import json
from django.utils import timezone
from admin_back.AdminPackage.querystring_parser import parser


# Create your views here.


def view_learn(request):
    params = {

    }
    check_login = login(request)

    if check_login == True:
        setting_obj = settings.objects.get(~Q(timezone=''))
        email = check_account(request, setting_obj.salt)

        get_sem_det = student_academic.objects.get(student_email=email)
        sem = get_sem_det.semester
        exp = get_sem_det.branch.split(":")

        get_br_post = post_content.objects.filter(status="Published", isSCP=True, SCP_program=exp[0], SCP_branch=exp[1], SCP_semester=sem)

        count_br = get_br_post.count()

        params['my'] = {}
        params['my'] = get_br_post

        


        return render(request, "student_html/post.html", params)

        

def view_post(request, view_post):
    pass    