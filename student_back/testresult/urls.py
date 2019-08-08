from django.urls import path
from . import views

urlpatterns = [
    path('student/test/details/<int:test_id>', views.test_details, name='signup')
]