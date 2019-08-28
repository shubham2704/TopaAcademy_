from django.urls import path
from . import views

urlpatterns = [
    path('student/exam/details/<int:test_id>', views.exam_details, name='Exam Details'),
    path('student/exam/session/<exam_session>', views.exam_started, name='Exam Session'),
    path('student/exam/session/<exam_session>/realtime', views.realtime_check, name='Exam Session Real Time Check'),
    path('student/exam/session/realtime_update/cron', views.realtime_check_cron, name='Real Time Cron - Run every 10 second'),
    path('student/exam/session/<exam_session>/realtime_question/<int:total>/<int:current>', views.realtime_question, name='Count  question in exam')
]