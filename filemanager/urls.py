from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # My Files
    path('files/', views.file_list, name='file_list'),

    # Upload Files
    path('upload/', views.upload_file, name='upload'),

    # Download File
    path('download/<str:filename>/', views.download_file, name='download_file'),

    # Delete File
    path('delete/<str:filename>/', views.delete_file, name='delete_file'),
]