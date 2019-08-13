from django.urls import path
from . import views

urlpatterns = [
    
    path('student/test/start/<int:test_id>', views.startsession, name='Start test session'),
    path('student/test/session/<test_session_id>', views.testing_session, name='Testing session'),
]