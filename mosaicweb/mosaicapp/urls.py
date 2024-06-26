from django.urls import path
from .views import hello_world
from .views import card_list
from .views import card_form
from .views import log_view
from .views import display_yaml

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('card-list/', card_list, name='card_list'),
    path('card-form/', card_form, name='card_form'),
    path('logs/', log_view, name='log_view'),
    path('data-catalog/', display_yaml, name='data_catalog'),
]