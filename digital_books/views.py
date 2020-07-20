from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from digital_books.forms import BookForm, CommentForm
from digital_books.models import Book, Comment
from digital_books.helpers import scrap_html, random_color, get_sort_title, letters, hold_notification_email
from custom_user.models import CustomUser


def index(request):
    """Displays books available for checkout or holds.  Allows for filtering
    displayed results."""
    books = Book.objects.all()

    sort_by = request.GET.get('sort')
    if sort_by == "author":
        books = books.order_by("author_last", "author_first")
    elif sort_by == "sort_title":
        books = books.order_by("sort_title")

    title_filter_by = request.GET.get('title_filter')
    if title_filter_by:
        if title_filter_by == 'other':
            books = books.filter(sort_title__iregex=r'^[^a-z].*')
        else:
            books = books.filter(sort_title__istartswith=title_filter_by)

    author_filter_by = request.GET.get('author_filter')
    if author_filter_by:
        if author_filter_by == 'other':
            books = books.filter(author_last__iregex=r'^[^a-z].*')
        else:
            books = books.filter(author_last__istartswith=author_filter_by)

    language_filter_by = request.GET.get('language')
    if language_filter_by:
        books = books.filter(language=language_filter_by)

    languages = sorted(list({book.language for book in Book.objects.all()}))
    color = random_color
    return render(request, 'digital_books/index.html', {

        'books': books,
        'color': color,
        'letters': letters(),
        'languages': languages
    })


class CreateBook(LoginRequiredMixin, View):
    """If the user is a librarian, allows the user to create
    a new book manually."""

    def get(self, request):
        if request.user.is_librarian is False:
            return HttpResponseRedirect(reverse('all_books'))
        form = BookForm()
        return render(request, 'digital_books/book_form.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Book.objects.create(
                title=data['title'],
                author_last=data['author_last'],
                author_first=data['author_first'],
                description=data['description'],
                URL=data['URL'],
                language=data['language'].title(),
                sort_title=get_sort_title(data['title'])
            )
            return HttpResponseRedirect(reverse('all_books'))


@login_required
def createGutenberg(request):
    """Allows the user to automatically look up a book's details when
    given the HTML address from gutenberg.org"""

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Book.objects.create(
                title=data['title'],
                author_first=data['author_first'],
                author_last=data['author_last'],
                description=data['description'],
                URL=data['URL'],
                language=data['language'].title(),
                sort_title=get_sort_title(data['title'])
            )
            return HttpResponseRedirect(reverse('all_books'))

    projectg = request.POST['projectg']
    (new_title, new_author_first, new_author_last, _,
     new_language, new_description) = scrap_html(
        projectg)

    form = BookForm(initial={
        'title': new_title,
        'author_first': new_author_first,
        'author_last': new_author_last,
        'description': new_description,
        'URL': projectg,
        'language': new_language,
    })

    return render(request, 'digital_books/book_form.html', {
        'form': form,
        'show_gutenberg': True
    })


@login_required
def delete_book(request, id):
    """Deletes a specific book object"""

    if request.user.is_superuser:
        book = Book.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect(reverse('all_books'))


@login_required
def update_book(request, id):
    """Allows the user to update a specific book object"""

    if request.user.is_superuser:
        book = Book.objects.get(id=id)
        if request.method == "POST":
            form = BookForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                book.title = data['title']
                book.author_first = data['author_first'],
                book.author_last = data['author_last'],
                book.description = data['description']
                book.URL = data['URL']
                book.language = data['language'].title()
                book.sort_title = data['sort_title']
                book.save()
                return HttpResponseRedirect(reverse(
                    'detail_book', args=(id, )))

        form = BookForm(initial={
            'title': book.title,
            'author_last': book.author_last,
            'author_first': book.author_first,
            'description': book.description,
            'URL': book.URL,
            'language': book.language,
            'sort_title': book.sort_title
        })
        return render(request, 'digital_books/book_form.html', {
            'form': form,
            'show_gutenberg': True
        })


class DetailBook(View):
    """Displays the details of a specific book"""

    def get(self, request, id):
        book = Book.objects.get(id=id)
        comments = Comment.objects.filter(book=book).order_by('-date')

        if request.user.is_authenticated:
            form = CommentForm()
            usr = CustomUser.objects.get(id=request.user.id)
            checkout = False
            if usr in book.checked_out.all():
                checkout = True
            held = book.holds.filter(id=request.user.id).exists()
            line_number = 23
            if held is True:
                for index, item in enumerate(Book.objects.get(id=id)
                                             .holdorder_set.all()):
                    if item.user == request.user:
                        line_number = index + 1
        else:
            return render(request, 'digital_books/book_detail.html', {
                'book': book,
                'comments': comments
            })

        return render(request, 'digital_books/book_detail.html', {
            'book': book,
            'checkout': checkout,
            'held': held,
            'line_number': line_number,
            'comments': comments,
            'form': form
        })

    def post(self, request, id):
        usr = CustomUser.objects.get(id=request.user.id)
        book = Book.objects.get(id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                author=usr,
                book=book,
                message=data['message']
            )

            return HttpResponseRedirect(reverse('detail_book', args=[id]))


@login_required
def checkout_book(request, id):
    """Allows the user to check out the book to their user account."""

    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.checked_out.add(usr)
    try:
        book.save()
    except Exception:
        book.checked_out.remove(usr)
        book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


@login_required
def checkin_book(request, id):
    """Allows a user to return a book to the 'shelves', so that it
    is no longer checked out to their account.  Automatically checks
    the book out to the next person in the hold list."""

    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.checked_out.remove(usr)
    if book.holds.exists():
        next_hold = book.holdorder_set.all()[0].user
        book.holds.remove(next_hold)
        book.checked_out.add(next_hold)
        hold_notification_email(next_hold, book)
    book.save()
    return HttpResponseRedirect(request.GET.get(
        'next', reverse('detail_book', args=(id,))))


@login_required
def hold_book(request, id):
    """Allows a user to place a 'hold' on the book, so that it will be
    checked out when it becomes available again."""

    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.holds.add(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


@login_required
def remove_hold_book(request, id):
    """Cancels the hold that a user placed on a particular book.
    The user will no longer be associated with the 'holds' field
    on the book."""

    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.holds.remove(usr)
    book.save()
    return HttpResponseRedirect(request.GET.get('next', reverse('detail_book', args=(id, ))))


def error404(request, exception):
    return render(request, '404.html', status=404)


def error500(request):
    return render(request, '500.html', status=500)
