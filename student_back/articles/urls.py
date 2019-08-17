from django.urls import path
from . import views

urlpatterns = [
    path('student/learning/', views.view_learn, name='Learning Center'),
    path('student/learning/<int:post_id>', views.view_post, name='View Learning POST'),

]