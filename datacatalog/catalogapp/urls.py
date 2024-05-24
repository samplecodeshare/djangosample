from django.urls import path
from .views import edit_yaml, display_yaml, list_yaml_files,display_yaml

urlpatterns = [
    path('list/', list_yaml_files, name='list_yaml_files'),
    path('edit/', edit_yaml, name='edit_yaml'),
    # path('display/', display_yaml, name='display_yaml'),
    path('view/<str:filename>/', display_yaml, name='display_yaml'),
]
