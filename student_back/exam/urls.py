from django.urls import path
from . import views

urlpatterns = [
    path('student/exam/details/<int:test_id>', views.exam_details, name='signup')
]