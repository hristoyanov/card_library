from django.urls import path
from main.views import index, expansion_set_list, expansion_card_list, card_info, custom_user_collection, add_card

urlpatterns = [
    path('', index, name='index'),
    path('sets/', expansion_set_list, name='set_list'),
    path('sets/<int:pk>/', expansion_card_list, name='card_list'),
    path('cards/<int:pk>/', card_info, name='card_info'),
    path('users/<int:pk>/', custom_user_collection, name='user_collection'),
    path('cards/add/<int:pk>/', add_card, name='add_card'),
]
