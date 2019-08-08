from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/settings', views.settings_call, name='settings_call')
]