from django.urls import path

from profiles.views import user_profile, change_profile_picture

urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    path('profile/change-picture/', change_profile_picture, name='change_picture'),
    path('profile/change-picture/<int:pk>/', change_profile_picture, name='change_picture'),
]
