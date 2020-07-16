from django.core.management.base import BaseCommand
from digital_books.models import Book
from digital_books.helpers import scrap_html, get_sort_title
import random


class Command(BaseCommand):
    """Allows for easy set-up of a library.  Typing
    'python manage.py populate_books <int>'
    will populate the library with at least that many
    books from project gutenberg.  Can be run when the library
    already has books in it."""

    help = 'Populate a desired number of random eBooks from Project Gutenberg'

    def add_arguments(self, parser):
        parser.add_argument('num_books', nargs='+', type=int)

    def handle(self, *args, **options):
        description = r'\b(The )?Project Gutenberg[\w\W\n]*(gutenberg.org|gutenberg.net|before using this ebook.)'
        n = int(options['num_books'][0])
        if n < 0:
            raise AssertionError(
                "Number of books cannot be a negative integer")
        while n:
            random_num = random.randint(1, 61000)
            url = "http://www.gutenberg.org/files/{}/{}-h/{}-h.htm".format(
                random_num, random_num, random_num)
            try:
                title, author_first, author_last, _, language, description = scrap_html(
                    url)
                book = Book.objects.create(
                    title=title,
                    author_first=author_first,
                    author_last=author_last,
                    description=description,
                    URL=url,
                    language=language,
                    sort_title=get_sort_title(title))
                book.save()
                del book
                self.stdout.write(self.style.SUCCESS(
                    'Successfully eBook added eBook["%s"].' % random_num))
                n -= 1
            except:
                pass
