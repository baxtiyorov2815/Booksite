from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Author, Genre, Book, BookRate

class Bookadmin(ModelAdmin):
    list_display = ('title', 'price', 'author', 'amount', 'created_at', 'updated_at')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_filter = ('created_at', 'updated_at')

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookRate)
admin.site.register(Book, Bookadmin)