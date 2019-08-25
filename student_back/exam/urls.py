from django.urls import path
from . import views

urlpatterns = [
    path('student/exam/details/<int:test_id>', views.exam_details, name='Exam Details'),
    path('student/exam/session/<exam_session>', views.exam_started, name='Exam Session')
]