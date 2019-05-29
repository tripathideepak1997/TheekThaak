from django import forms
choices = [(i, str(i)) for i in range(1, 4)]


class UpdateCartForm(forms.Form):
    quantity = forms.ChoiceField(choices=choices)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)