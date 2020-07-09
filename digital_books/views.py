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
            new_book = Book.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                URL=data['URL']
            )
            new_book.save()
            return HttpResponseRedirect(reverse('all_books'))

    form = BookForm()
    return render(request, 'digital_books/book_form.html', {'form': form})


def createGutenberg(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_book = Book.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                URL=data['URL']
            )
            new_book.save()
            return HttpResponseRedirect(reverse('all_books'))

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
    checkout = False
    if usr in book.checked_out.all():
        checkout = True
    held = book.holds.filter(id=request.user.id).exists()
    line_number = 23
    if held == True:
        qs = Book.objects.get(id=id).holdorder_set.all()
        for index, item in enumerate(Book.objects.get(id=id).holdorder_set.all()):
            
            line_number = 3
            if item.user == request.user:
                line_number = index + 1
       

    return render(request, 'digital_books/book_detail.html', {
        'book': book,
        'checkout': checkout,
        'held': held,
        'line_number': line_number
    })


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


def checkin_book(request, id):
    book = Book.objects.get(id=id)
    usr = CustomUser.objects.get(id=request.user.id)
    book.checked_out.remove(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))


                    
def hold_book(request, id):
    book = Book.objects.get(id=id) 
    usr = CustomUser.objects.get(id=request.user.id)   
    book.holds.add(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))

def remove_hold_book(request, id):
    book = Book.objects.get(id=id) 
    usr = CustomUser.objects.get(id=request.user.id)   
    book.holds.remove(usr)
    book.save()
    return HttpResponseRedirect(reverse('detail_book', args=(id, )))