from django.urls import path
from main_auth.views import RegisterView, login_user, logout_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]
