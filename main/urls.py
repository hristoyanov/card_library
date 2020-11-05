from django.urls import path
from main.views import index, about, expansion_set_list, expansion_card_list

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('sets/', expansion_set_list, name='set_list'),
    path('sets/<int:pk>/', expansion_card_list, name='card_list'),
]
