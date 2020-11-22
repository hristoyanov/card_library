from django.urls import path
from main.views import index, expansion_set_list, expansion_card_list, card_info, user_collection, \
    add_card, increase_collected_card_count, remove_collected_card_copies, delete_collection_card

urlpatterns = [
    path('', index, name='index'),
    path('sets/', expansion_set_list, name='set_list'),
    path('sets/<int:pk>/', expansion_card_list, name='card_list'),
    path('cards/<int:pk>/', card_info, name='card_info'),
    path('cards/add/<int:pk>/', add_card, name='add_card'),
    path('my-collection/', user_collection, name='user_collection'),
    path('my-collection/filtered/', user_collection, name='collected_set_cards'),
    path('my-collection/add/<int:pk>/', increase_collected_card_count, name='add_copies'),
    path('my-collection/remove/<int:pk>/', remove_collected_card_copies, name='remove_copies'),
    path('my-collection/delete/<int:pk>/', delete_collection_card, name='delete_user_card'),
]
