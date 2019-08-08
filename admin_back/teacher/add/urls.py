from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/staff/add', views.add, name='Teacher Add'),
]