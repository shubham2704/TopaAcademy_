from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/login', views.login, name='login'),
]