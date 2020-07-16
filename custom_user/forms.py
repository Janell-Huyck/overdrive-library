from .models import CustomUser
from django import forms


class SignupForm(forms.ModelForm):

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }
        model = CustomUser
        fields = ('username', 'display_name',
                  'email', 'password', 'is_librarian')


class LoginForm(forms.Form):
    identification = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
