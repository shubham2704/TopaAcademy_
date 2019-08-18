from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/post/add', views.post_add, name='Post Add'),
    
    path('admin-panel/post/', views.post_view, name='Posts Add'),
    path('admin-panel/post/edit/<int:post_id>', views.post_edit, name='Posts Add'),
    path('admin-panel/post/delete/<int:post_id>', views.post_delete, name='Posts Add'),
    path('admin-panel/post/test/ajax/<sct_bool>/<steam>/<branch>', views.sct_ajax, name='Test'),
    path('admin-panel/post/ajax/steam/<sid>', views.ajax_steam, name='Post Add'),
    path('admin-panel/post/test/ajax-steam-dual/<id>/<name>', views.steam_dual_ajax, name='Test'),
    path('admin-panel/post/upload/<ses_id>', views.upload_file, name='Upload file'),
    path('admin-panel/post/ajax/del_file/<int:file_id>/<ses_id>', views.file_delete, name='Delete file'),
]