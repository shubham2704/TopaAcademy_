from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/user/admin', views.admin_view, name='Admin Account Managment'),
    path('admin-panel/account', views.admin_account, name='Admin Account'),
    path('admin-panel/web_setup', views.setup_first, name='Web Setup'),
    path('admin-panel/user/admin/manage/<action>/<int:user_id>', views.admin_edit, name='Admin Manage'),
]