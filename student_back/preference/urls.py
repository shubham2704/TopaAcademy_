from django.urls import path
from . import views

urlpatterns = [
    path('student/preference', views.preference, name='Preference')
]