"""
URL configuration for mosaicweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from api.views import get_cards
from api.views import get_card_params
from api.views import generate_download_link, download_file


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mosaicapp.urls')),
    path('api/cards/', get_cards, name='get_cards'),
    path('api/cardparams/', get_card_params, name='get_card_params'),
    path('api/submit/', generate_download_link, name='generate_download_link'),
    path('downloads/<str:file_name>/', download_file, name='download_file'),
]
