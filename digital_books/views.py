from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, reverse
from digital_books.forms import BookForm
from digital_books.models import Book
from digital_books.helpers import scrap_html
from custom_user.models import CustomUser


# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'digital_books/index.html', {'books': books})


def search(request):
    # books = BookModel.objects.all().order_by('title')
    # return render(request, 'digital_books/search.html', {'books': books})
    return render(request, 'digital_books/search.html')


def createBook(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Book.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                URL=data['URL']
            )
            return HttpResponseRedirect(reverse('home'))

    form = BookForm()
    return render(request, 'digital_books/book_form.html', {'form': form})


def createGutenberg(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Book.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                URL=data['URL']
            )
            return HttpResponseRedirect(reverse('home'))

    projectg = request.POST['projectg']
    new_title, new_author = scrap_html(projectg)

    form = BookForm(initial={
        'title': new_title,
        'author': new_author,
        'URL': projectg
    })

    return render(request, 'digital_books/book_form.html', {
        'form': form,
        'show_gutenberg': True
    })


def detail_book(request, id):
    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    return render(request, 'digital_books/book_detail.html', {'book': book})
