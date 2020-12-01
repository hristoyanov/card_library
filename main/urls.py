from django.urls import path
from main.views.public_views import index, ExpansionSetListView, ExpansionSetCardListView, CardDetailView
from main.views.user_views import add_card, user_collection, missing_cards_list, increase_collected_card_count, \
    remove_collected_card_copies, delete_collection_card

urlpatterns = [
    path('', index, name='index'),
    path('sets/', ExpansionSetListView.as_view(), name='set_list'),
    path('sets/<int:pk>/', ExpansionSetCardListView.as_view(), name='card_list'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('cards/add/<int:pk>/', add_card, name='add_card'),
    path('my-collection/', user_collection, name='user_collection'),
    path('my-collection/missing/', missing_cards_list, name='missing'),
    path('my-collection/add/<int:pk>/', increase_collected_card_count, name='add_copies'),
    path('my-collection/remove/<int:pk>/', remove_collected_card_copies, name='remove_copies'),
    path('my-collection/delete/<int:pk>/', delete_collection_card, name='delete_user_card'),
]
