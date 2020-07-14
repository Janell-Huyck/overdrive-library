from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from digital_books.forms import BookForm
from digital_books.models import Book
from digital_books.helpers import scrap_html, random_color
from custom_user.models import CustomUser


# Create your views here.
def index(request):
    books = Book.objects.all()
    color = random_color
    return render(request, 'digital_books/index.html', {
        'books': books,
        'color': color
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
                author=data['author'],
                description=data['description'],
                URL=data['URL'],
                language=data['language'].title()
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
                author=data['author'],
                description=data['description'],
                URL=data['URL'],
                language=data['language'].title()
            )
            return HttpResponseRedirect(reverse('all_books'))

    projectg = request.POST['projectg']
    new_title, new_author, _, new_language, new_description = scrap_html(
        projectg)

    form = BookForm(initial={
        'title': new_title,
        'author': new_author,
        'description': new_description,
        'URL': projectg,
        'language': new_language
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


class DetailBook(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        usr = CustomUser.objects.get(id=request.user.id)
        checkout = False
        if usr in book.checked_out.all():
            checkout = True
        held = book.holds.filter(id=request.user.id).exists()
        line_number = 23
        if held is True:
            qs = Book.objects.get(id=id).holdorder_set.all()
            for index, item in enumerate(Book.objects.get(id=id).holdorder_set.all()):
                if item.user == request.user:
                    line_number = index + 1

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
    except:
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
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


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
