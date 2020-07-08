from .models import CustomUser
from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=60)
    display_name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254)


class LoginForm(forms.ModelForm):

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }
        model = CustomUser
        fields = ('library_card_number', 'password',)
