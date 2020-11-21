from django import forms


class ChangeCardCountForm(forms.Form):
    count = forms.IntegerField(initial=1, min_value=1, label='Copies')
