from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/user/admin', views.admin_view, name='steam'),
    path('admin-panel/user/admin/manage/<action>/<int:user_id>', views.admin_edit, name='steam'),
]