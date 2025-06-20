from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .authentications import CustomAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    AuthorListCreateAPIView,
    AuthorListAPIView,
    AuthorDeleteAPIView,
    AuthorRetrieveAPIView,
    AuthorRetrieveUpdateDeleteAPIView,
    GenresListAPIView,
    GenreListAPIView,
    UsersListAPIView,
    UserListAPIView,
    BookListAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDeleteAPIView,
    BookRetrieveAPIView
    # AuthorDetailAPIView,
    # GenreListCreateAPIView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', CustomAuthToken.as_view(), name='api_auth'),
    # path('authors/', get_authors, name='get_authors'),
    # path('genres/', get_genres, name='get_genres'),
    # path('books/', get_books, name='get_books'),
    # path('users/', get_users, name='get_users'),
    path('api-auth/', include('rest_framework.urls')),
    path('authors/list/', AuthorListAPIView.as_view(), name='authors_list'),
    path('authors/list/create/', AuthorListCreateAPIView.as_view(), name='authors_list_create'),
    path('authors/delete/<int:pk>/', AuthorDeleteAPIView.as_view(), name='authors_delete'),
    path('authors/retrieve/<int:pk>/', AuthorRetrieveAPIView.as_view(), name='authors_retrieve'),
    path('authors/all/<int:pk>/', AuthorRetrieveUpdateDeleteAPIView.as_view(), name='authors_all'),
    path('genres/', GenresListAPIView.as_view(), name='genres'),
    path('genre/<int:pk>/', GenreListAPIView.as_view(), name='genre'),
    path('users/', UsersListAPIView.as_view(), name='users'),
    path('user/<int:pk>/', UserListAPIView.as_view(), name='user'),
    path('books/', BookListAPIView.as_view(), name='books'),
    path('book/create/', BookListCreateAPIView.as_view())
    # path('author/<int:pk>/', AuthorDetailAPIView.as_view(), name='author_detail'),
    # path('genres/', GenreListCreateAPIView.as_view(), name='genres')
]

urlpatterns = format_suffix_patterns(urlpatterns)