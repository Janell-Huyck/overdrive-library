from .models import CustomUser
from django import forms


class SignupForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'display_name',
                  'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control short'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control short'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control short'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control short'
            }),
        }


class LoginForm(forms.Form):
    identification = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
