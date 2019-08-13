from django.shortcuts import render, redirect
from admin_back.admin_main.models import test_data, test_details_advanced, test_details
from admin_back.websettings.models import settings
from django.core.signing import Signer
from django.db.models import Q
from django.contrib import messages
from admin_back.websettings.models import settings
from admin_back.steam.models import Steam, Steam_Data
from ..GlobalModels.main import login, check_account
