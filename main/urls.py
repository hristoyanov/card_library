from django.urls import path
from main.views import index, about, expansion_set_list, expansion_card_list, card_info

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('sets/', expansion_set_list, name='set_list'),
    path('sets/<int:pk>/', expansion_card_list, name='card_list'),
    path('cards/<int:pk>/', card_info, name='card_info')
]
