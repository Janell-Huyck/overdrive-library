from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=60)
    displayname = forms.CharField(max_length=60)
    password = forms.CharField(widget=forms.PasswordInput)
