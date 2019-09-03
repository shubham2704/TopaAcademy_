from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/login', views.login, name='Admin login'),
    path('admin-panel/logout', views.logout, name='Admin logout'),
]