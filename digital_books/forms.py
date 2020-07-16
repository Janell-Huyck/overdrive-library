from django import forms
from digital_books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author_last',
                  'author_first', 'description', 'URL', 'language']
