from django.urls import path
from . import views

urlpatterns = [
    path('student/signup', views.signup, name='signup')
]