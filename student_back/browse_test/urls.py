from django.urls import path
from . import views

urlpatterns = [
    path('student/test/browse', views.browse, name='Browse Test'),
    path('student/test/browse/ajax-steam/<int:steam_id>', views.steam_ajax, name='Browse Test'),
    path('student/test/browse/ajax-steam-dual/<id>/<name>', views.steam_dual_ajax, name='Test'),
    path('student/test/browse/ajax-browse/', views.ajax_browse, name='Test'),
]