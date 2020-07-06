from django.shortcuts import render
# from digital_books.models import BookModel


# Create your views here.
def index(request):
    return render(request, 'digital_books/index.html')


def search(request):
    # books = BookModel.objects.all().order_by('title')
    # return render(request, 'digital_books/search.html', {'books': books})
    return render(request, 'digital_books/search.html')
