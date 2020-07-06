from django.shortcuts import render
from custom_user.models import CustomUser


# Create your views here.
def index(request):
    return render(request, 'custom_user/index.html')


def profile(request):
    custom_user = CustomUser.objects.get(
        library_card_number=request.user.library_card_number)
    return render(request, 'custom_user/profile.html', {'custom_user': custom_user})
