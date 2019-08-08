from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.index),
    path('student/otp/<int:number>', views.otp_send),
    path('student/email_verification/', views.email_verification),
]