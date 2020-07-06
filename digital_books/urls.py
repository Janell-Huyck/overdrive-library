from django.urls import path
from digital_books import views

urlpatterns = [
    path('', views.search, name='search'),
]
