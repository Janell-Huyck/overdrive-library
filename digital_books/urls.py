from django.urls import path
from digital_books import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.createBook, name='create_book'),
    path('create/gutenberg/', views.createGutenberg, name='create_gutenberg'),
    path('<int:id>/', views.detail_book, name='detail_book'),
    path('<int:id>/checkout', views.checkout_book, name='checkout'),
    path('<int:id>/checkin', views.checkin_book, name='checkin'),
]
