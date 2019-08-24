from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/edit/test/<int:edit_id>', views.edit_test, name='edit_test'),
    path('admin-panel/edit/test/<int:edit_id>/QuestionBank', views.question_bank, name='Add Question Bank'),
    path('admin-panel/ajax_qb/test/<int:i>', views.add_qb_ajax, name='edit_test ajax')
]