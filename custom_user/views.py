from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, reverse
from custom_user.models import CustomUser
from custom_user.forms import SignupForm, LoginForm
from django.views.generic.base import View
from digital_books.models import Book
from django.contrib.auth.decorators import login_required


def createUser(request):
    """Allows new users to create an account, and after successful
    account creation logs them in."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            custom_user = CustomUser.objects.create(
                username=data['username'],
                password=data['password'],
                display_name=data['display_name'],
                email=data['email'],
                is_librarian=data['is_librarian']
            )
            custom_user.set_password(raw_password=data['password'])
            custom_user.save()

            custom_user = authenticate(
                request,
                username=data['username'],
                password=data['password'],
                display_name=data['display_name'],
                email=data['email'],
            )
            if custom_user:
                login(request, custom_user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home')))
    form = SignupForm()
    return render(request, 'custom_user/generic_form.html', {'form': form})


class Login(View):
    html = 'custom_user/login_form.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.html,
                      {"form": form})

    def post(self, request):
        username = ""
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                username = CustomUser.objects.get(
                    library_card_number=int(data['identification'])).username
            except Exception:
                try:
                    username = CustomUser.objects.get(
                        email=data['identification']
                    ).username
                except Exception:
                    username = data['identification']
            finally:
                current_user = authenticate(
                    username=username,
                    password=data['password']
                )

            if current_user:
                login(request, current_user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home')))
            else:
                print(username)
                render(request, self.html,
                       {"form": form,
                           "message_before": """Unable to authorize.
                                    Please check your information and
                                    try again."""})
        return render(request, self.html, {"form": form,
                                           "message_before": """Unable to authorize.
                                    Please check your information and
                                    try again."""})


@ login_required
def profile(request):
    """ For profile page - returns logged in user's profile data"""
    custom_user = CustomUser.objects.get(
        library_card_number=request.user.library_card_number)
    books_queryset_out = Book.objects.filter(
        checked_out__username__icontains=custom_user.username)
    books_out = [book for book in books_queryset_out]
    books_queryset_hold = Book.objects.filter(
        holds__username__icontains=custom_user.username)
    books_hold = [book for book in books_queryset_hold]
    return render(request,
                  'custom_user/profile.html',
                  {'custom_user': custom_user,
                   'books_out': books_out,
                   'books_hold': books_hold})


def index(request):
    return render(request, 'index.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
