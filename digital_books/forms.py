from django import forms
from digital_books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_last',
                  'author_first', 'description', 'URL', 'language']
        widgets = {
            'author_last': forms.TextInput(
                attrs={'placeholder': 'Last Name'}),
            'author_first': forms.TextInput(
                attrs={'placeholder': 'First Name'}),
        }
