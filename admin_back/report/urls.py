from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/report/monitor/exam/<exam_id>', views.monitor_exam, name='Post Add'),
    path('admin-panel/report/monitor/exam/<exam_id>/realtime', views.monitor_exam_realtime, name='Post Add'),
    path('admin-panel/report/exam', views.exam_report, name='Post Add'),
    
]