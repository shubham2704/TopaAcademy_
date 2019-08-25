"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('admin_back.index.urls')),
    path('', include('admin_back.students.urls')),
    path('', include('admin_back.login.urls')),
    path('', include('admin_back.steam.urls')),
    path('', include('admin_back.report.urls')),
    path('', include('admin_back.admin_main.urls')),
    path('', include('admin_back.post.urls')),
    path('', include('admin_back.announcement.urls')),
    path('', include('admin_back.Add_Admin.urls')),
    path('', include('admin_back.websettings.urls')),
    path('', include('admin_back.teacher.add.urls')),
    path('', include('admin_back.test_main.urls')),
    path('', include('admin_back.branch.urls')),
    path('', include('admin_back.session_manager.urls')),
    path('', include('student_back.index.urls')),
    path('', include('student_back.articles.urls')),
    path('', include('student_back.login.urls')),
    path('', include('student_back.exam.urls')),
    path('', include('student_back.preference.urls')),
    path('', include('student_back.view_test_info.urls')),
    path('', include('student_back.browse_test.urls')),
    path('', include('student_back.start_test.urls')),
    path('', include('student_back.signup.urls')),
    path('', include('teacher_back.index.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)