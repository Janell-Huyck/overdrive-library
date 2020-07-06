from django.shortcuts import render
# from custom_user.models import CustomUserModel


# Create your views here.
def index(request):
    return render(request, 'custom_user/index.html')


def profile(request):
    # my_user = CustomUserModel.objects.get(pk=request.pk)
    # return render(request, 'custom_user/profile.html', {'my_user': my_user})
    pass
