from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/session/', views.session_view, name='Session View'),
    path('admin-panel/session/modal/ajax/<int:id>', views.session_ajax_modal_view, name='Session View'),
    path('admin-panel/session/modal/ajax/update/<int:id>/<int:class_tchr>/<int:hod>', views.session_ajax_modal_update_view, name='Session View'),
]