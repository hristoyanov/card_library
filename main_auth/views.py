from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from main.models.class_portrait import ClassPortrait
from main_auth.forms import RegisterForm, LoginForm
from main_auth.models import UserProfile
from main_core.reusables import get_next_url


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm()

        return context

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            group = Group.objects.get(name='Regular User')
            user.groups.add(group)
            profile = UserProfile(user=user, profile_picture=ClassPortrait.objects.get(name='Default'))
            profile.save()

            login(request, user)
            return redirect('user_profile')

        return render(request, 'auth/register.html', context={'register_form': register_form})


def login_user(request):
    if request.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }

        return render(request, 'auth/login.html', context)
    else:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(get_next_url(request.POST))

            messages.error(request, 'Invalid login credentials!')
            errors = get_messages(request)

            context = {
                'login_form': login_form,
                'messages': errors,
            }

            return render(request, 'auth/login.html', context)

        return render(request, 'auth/login.html', context={'login_form': login_form})


class LogOutView(LogoutView):
    next_page = 'index'
