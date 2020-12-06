from django import forms

from main_auth.models import UserProfile


class FavouriteClassForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('favourite_class',)
