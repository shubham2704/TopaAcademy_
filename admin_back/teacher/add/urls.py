from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/staff/add', views.add, name='Saff Add'),
    path('admin-panel/staff/edit/<int:staff_id>', views.edit_saff, name='Saff Edit'),
]