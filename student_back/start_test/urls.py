from django.urls import path
from . import views

urlpatterns = [
    path('student/test/start/<int:test_id>', views.startsession, name='Start Session'),
]