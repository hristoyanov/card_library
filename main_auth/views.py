from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# Create your views here.
def login_view(request):
    user = authenticate(request, username='user1', password='trudnaparola1')

    if user:
        login(request, user)
        return redirect('index')

    return redirect('index')


def logout_view(request):
    logout(request)

    return redirect('index')
