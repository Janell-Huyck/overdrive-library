from django import forms
from digital_books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_last',
                  'author_first', 'description', 'URL', 'language']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'e.g. My First Picture Book',
                       'class': 'form-control'}),
            'author_last': forms.TextInput(
                attrs={'placeholder': 'Last Name',
                       'class': 'form-control col'}),
            'author_first': forms.TextInput(
                attrs={'placeholder': 'First Name',
                       'class': 'form-control col'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter a brief summary...',
                       'class': 'form-control',
                       'rows': 4}),
            'URL': forms.TextInput(
                attrs={'placeholder': 'e.g. http://www.gutenberg.org/files/62693/62693-h/62693-h.htm',
                       'class': 'form-control'}),
            'language': forms.TextInput(
                attrs={'placeholder': 'e.g. English',
                       'class': 'form-control'})
        }
