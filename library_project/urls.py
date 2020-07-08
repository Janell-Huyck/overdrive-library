"""library_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from custom_user import views as CUviews


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('digital_books/', include('digital_books.urls')),
    path('profile/', CUviews.profile, name='profile'),
    path('create_user/', CUviews.createUser, name='create_user'),
    path('login/', CUviews.Login.as_view(), name='login'),
    path('logoutview/', CUviews.logoutview, name='logoutview'),
    path('', CUviews.index, name='home')

]
