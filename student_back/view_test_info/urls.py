from django.urls import path
from . import views

urlpatterns = [
    path('student/test/details/<int:test_id>', views.test_details_view, name='Test Details'),
    path('student/test/start/<int:test_id>', views.startsession, name='Start test session'),
    path('student/exam/start/<int:test_id>', views.startsession_exam, name='Start Exam session'),
    path('student/test/session/<test_session_id>', views.testing_session, name='Testing session'),
]