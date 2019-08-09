from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/add/test', views.add_mock_test, name='Test'),
    path('admin-panel/test/', views.test_det, name='Test'),
    path('admin-panel/add/test/ajax/<sct_bool>/<steam>/<branch>', views.sct_ajax, name='Test'),
    path('admin-panel/add/test/ajax-steam/<steam_id>', views.steam_ajax, name='Test'),
    path('admin-panel/add/test/ajax-steam-dual/<id>/<name>', views.steam_dual_ajax, name='Test'),
]