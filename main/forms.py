from django import forms
from main.models.custom_user import CustomUser


class AddCardForm(forms.Form):
    copies_to_add = forms.IntegerField(initial=1, min_value=1)
    user = forms.ModelChoiceField(CustomUser.objects.all())
