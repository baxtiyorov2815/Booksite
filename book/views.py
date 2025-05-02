from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.views import View
from .models import Book, Author, Genre, BookRate
from django.db.models import Avg

class HomePageView(View):
    def get(self, request):
        new_books = Book.objects.all().order_by('-created_at')[:8]
        print(new_books)
        most_sold_books = Book.objects.all().order_by('-sold')[:8]
        most_rated_books = Book.objects.annotate(
                avg_rating=Avg('rates__rate')
                ).order_by('-avg_rating')[:8]
        # Assuming you want to get the first 8 books for each category
        return render(request, 'book/home.html', {'new_books': new_books, 
                                                'most_sold': most_sold_books,
                                                'most_rated': most_rated_books})

class BookDetailView(View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        is_new = book.created_at >= timezone.now() - timedelta(days=7)
        is_best_seller = book.sold >= 100
        discount = book.discount > 0
        discounted_price = float(book.price) * (1 - book.discount / 100) if book.discount > 0 else book.price
        genres = book.genres.all()
        return render(request, 'book/product.html', {'book': book, 'is_new': is_new, 'is_best_seller': is_best_seller, 'discount': discount, 'discounted_price': round(discounted_price, 2), 'genres': genres})

class GridPageView(View):
    def get(self, request):
        books = Book.objects.all()
        genres = Genre.objects.all()
        authors = Author.objects.all()

        selected_genres = request.GET.getlist('genre')
        print(selected_genres)
        selected_author = request.GET.get('author')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if selected_genres:
            books = books.filter(genres__id__in=selected_genres).distinct()
        if selected_author=="all":
            books = Book.objects.all()
        elif selected_author:
            books = books.filter(author__id=selected_author)
        if min_price:
            books = books.filter(price__gte=min_price)
        if max_price:
            books = books.filter(price__lte=max_price)
 
 
        return render(request, 'book/grid.html', {'books': books, 'genres': genres, 'authors': authors, 'selected_genre': selected_genres, 'selected_author': selected_author})