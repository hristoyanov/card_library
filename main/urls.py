from django.urls import path
from main.views import index, expansion_set_list, expansion_card_list, card_info, user_collection, \
    add_card, increase_collected_card_count, remove_collected_card_copies, delete_collection_card

urlpatterns = [
    path('', index, name='index'),
    path('sets/', expansion_set_list, name='set_list'),
    path('sets/<int:pk>/', expansion_card_list, name='card_list'),
    path('cards/<int:pk>/', card_info, name='card_info'),
    path('cards/add/<int:pk>/', add_card, name='add_card'),
    path('my-cards/', user_collection, name='user_collection'),
    path('my-cards/add/<int:pk>/', increase_collected_card_count, name='add_copies'),
    path('my-cards/remove-copies/<int:pk>/', remove_collected_card_copies, name='remove_copies'),
    path('my-cards/delete/<int:pk>/', delete_collection_card, name='delete_user_card'),
]
