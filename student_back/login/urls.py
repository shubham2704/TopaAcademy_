from django.urls import path
from . import views

urlpatterns = [
    path('student/login', views.login, name='signup')
]