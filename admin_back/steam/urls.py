from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/steam', views.steam, name='steam'),
    path('admin-panel/steam/<action_name>/<int:perform_action_on_id>', views.CallAction),
]