from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from main.models.class_portrait import ClassPortrait
from profiles.forms import FavouriteClassForm


@login_required
def user_profile(request):
    user = request.user
    cards = user.collectioncard_set.distinct('card__expansion_set')

    if request.method == 'GET':
        context = {
            'profile_user': user,
            'profile': user.userprofile,
            'form': FavouriteClassForm(),
            'favourite_class': user.userprofile.favourite_class,
            'cards': cards,
        }

        return render(request, 'auth/user_profile.html', context)
    else:
        form = FavouriteClassForm(request.POST, instance=user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('user_profile')

        return redirect('user_profile')


@login_required
def change_profile_picture(request, pk=None):
    if request.method == 'GET':
        classes = ClassPortrait.objects.all()

        return render(request, 'profiles/change_picture.html', context={'classes': classes})
    else:
        user = request.user
        class_picture = ClassPortrait.objects.get(pk=pk)

        user.userprofile.profile_picture = class_picture
        user.userprofile.save()

        return redirect('user_profile')
