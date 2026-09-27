from django.urls import path
from . import views

urlpatterns = [
    path('books/',          views.api_books,       name='api_books'),
    path('books/<int:pk>/', views.api_book_detail, name='api_book_detail'),
]
