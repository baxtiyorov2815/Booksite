from django.urls import path

from .views import BookSearchAPIView

urlpatterns = [
    path("", BookSearchAPIView.as_view(), name='book_search'),
]