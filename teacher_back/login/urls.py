from django.urls import path
from . import views

urlpatterns = [
    path('teacher/login', views.login),
    path('teacher/logout', views.logout),
]