from .models import CustomUser
from django import forms


class SignupForm(forms.ModelForm):

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }
        model = CustomUser
        fields = ('username', 'display_name', 'email', 'password', )


class LoginForm(forms.Form):

    username = forms.CharField(max_length=60, required=False)
    library_card_number = forms.IntegerField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
