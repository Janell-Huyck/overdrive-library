from django.urls import path
from digital_books import views

urlpatterns = [
    path('all_books', views.index, name='all_books'),
    path('create/', views.createBook, name='create_book'),
    path('create/gutenberg/', views.createGutenberg, name='create_gutenberg'),
    path('<int:id>/delete/', views.delete_book, name='delete_book'),
    path('<int:id>/', views.detail_book, name='detail_book'),
    path('<int:id>/checkout', views.checkout_book, name='checkout'),
    path('<int:id>/checkin', views.checkin_book, name='checkin'),
    path('<int:id>/hold', views.hold_book, name='hold'),
    path('<int:id>/remove_hold', views.remove_hold_book, name='remove_hold'),
]
