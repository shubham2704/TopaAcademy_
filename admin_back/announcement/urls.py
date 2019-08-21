from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/announcement', views.announcement_view, name='Announcement'),
]