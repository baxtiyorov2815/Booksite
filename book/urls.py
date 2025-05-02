from django.urls import path
from .views import HomePageView, BookDetailView, GridPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('grid/', GridPageView.as_view(), name='grid'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
]