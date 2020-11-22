from django import forms
from main.models.expansion_set import ExpansionSet


class ChangeCardCountForm(forms.Form):
    count = forms.IntegerField(initial=1, min_value=1, label='Copies')


class SelectExpSetForm(forms.Form):
    expansion_set = forms.ModelChoiceField(ExpansionSet.objects.all(), label='Select Expansion Set')
