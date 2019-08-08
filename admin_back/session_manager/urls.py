from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/session/', views.session_view, name='Session View'),
]