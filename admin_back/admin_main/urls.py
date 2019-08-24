from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/add/test', views.add_mock_test, name='Test'),
    path('admin-panel/test/', views.test_det, name='Test'),
    path('admin-panel/add/test/exam', views.conduct_exam, name='Test Action'),
    path('admin-panel/test/action', views.test_action, name='Test Action'),
    path('admin-panel/test/action/exam_eligability/<int:test_id>', views.exam_eligability, name='Test Action'),
    path('admin-panel/test/action/exam_eligability_create/<int:test_id>', views.exam_eligability_create, name='Test Action'),
    path('admin-panel/add/test/ajax/<sct_bool>/<steam>/<branch>', views.sct_ajax, name='Test'),
    path('admin-panel/add/test/ajax-steam/<steam_id>', views.steam_ajax, name='Test'),
    path('admin-panel/add/test/ajax-steam-dual/<id>/<name>', views.steam_dual_ajax, name='Test'),
]