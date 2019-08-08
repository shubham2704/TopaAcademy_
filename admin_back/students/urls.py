from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/students/', views.student_view, name='Post Add'),
    path('admin-panel/students/view/<int:sid>', views.student_profile_view, name='Posts Add')
]