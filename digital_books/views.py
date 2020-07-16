from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from digital_books.forms import BookForm
from digital_books.models import Book
from digital_books.helpers import scrap_html, random_color, get_sort_title
from custom_user.models import CustomUser


def index(request):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z']

    books = Book.objects.all()

    sort_by = request.GET.get('sort')
    if sort_by == "author":
        books = books.order_by("author_last", "author_first")
    elif sort_by == "sort_title":
        books = books.order_by("sort_title")

    title_filter_by = request.GET.get('title_filter')
    if title_filter_by:
        books = books.filter(
            sort_title__istartswith=title_filter_by)

    author_filter_by = request.GET.get('author_filter')
    if author_filter_by:
        books = books.filter(
            author_last__istartswith=author_filter_by)

    color = random_color
    return render(request, 'digital_books/index.html', {

        'books': books,
        'color': color,
        'letters': letters
    })


class CreateBook(LoginRequiredMixin, View):
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
    if request.user.is_superuser:
        book = Book.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect(reverse('all_books'))


@login_required
def update_book(request, id):
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
    def get(self, request, id):
        book = Book.objects.get(id=id)

        if request.user.is_authenticated:
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
            return render(request, 'digital_books/book_detail.html', {'book': book})

        return render(request, 'digital_books/book_detail.html', {
            'book': book,
            'checkout': checkout,
            'held': held,
            'line_number': line_number
        })


@login_required
def checkout_book(request, id):
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
    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.checked_out.remove(usr)
    if book.holds.exists():
        next_hold = book.holdorder_set.all()[0].user
        book.holds.remove(next_hold)
        book.checked_out.add(next_hold)
    book.save()
    return HttpResponseRedirect(request.GET.get('next', reverse('detail_book', args=(id,))))


@login_required
def hold_book(request, id):
    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.holds.add(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


@login_required
def remove_hold_book(request, id):
    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.holds.remove(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


def error404(request, exception):
    return render(request, '404.html', status=404)


def error500(request):
    return render(request, '500.html', status=500)
