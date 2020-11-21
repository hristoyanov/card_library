from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from main_auth.forms import RegisterForm, LoginForm


def get_redirect_url(params):
    redirect_url = params.get('return_url')
    return redirect_url if redirect_url else 'index'


def register_user(request):
    if request.method == 'GET':
        context = {
            'register_form': RegisterForm(),
        }

        return render(request, 'auth/register.html', context)
    else:
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            group = Group.objects.get(name='Regular User')
            user.groups.add(group)

            login(request, user)
            return redirect('index')

        context = {
            'register_form': register_form,
        }

        return render(request, 'auth/register.html', context)


def login_user(request):
    if request.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }

        return render(request, 'auth/login.html', context)
    else:
        login_form = LoginForm(request.POST)
        return_url = get_redirect_url(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(return_url)

        context = {
            'login_form': login_form,
        }

        return render(request, 'auth/login.html', context)


@login_required
def logout_user(request):
    logout(request)

    return redirect('index')
