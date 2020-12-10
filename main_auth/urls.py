from django.urls import path
from main_auth.views import RegisterView, login_user, LogOutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', LogOutView.as_view(), name='logout_user'),
]

from .receivers import *
