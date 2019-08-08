from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/branch', views.branch, name='branch'),
    path('admin-panel/branch/delete/<int:degree_id>', views.del_degree, name='branch'),
    path('admin-panel/branch/edit/<int:degree_id>', views.edit_degree, name='branch'),
    path('admin-panel/branch/edit/<int:degree_id>/branch/delete/<int:branch_id>', views.del_branch, name='branch'),
]