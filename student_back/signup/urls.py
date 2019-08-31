from django.urls import path
from . import views

urlpatterns = [
    path('student/signup', views.signup, name='signup'),
    path('student/verify_email/<act_hash>', views.activate_account, name='Account Activation')
]