from .serializers import AuthorSerializer, GenreSerializer, BookSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from book.models import Author, Genre, Book
from accounts.models import CustomUser
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsStaff, IsStaffOrReadOnly, IsAdminOrReadOnlyForStaff
from rest_framework import authentication

from .mixins import UserQuerySetMixin

# @api_view(['GET', 'POST', 'DELETE'])
# def get_authors(request):
#     if request.method == "GET":
#         authors = Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = AuthorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
        
#     elif request.method == "DELETE":
#         author_id = request.data.get('id')
#         try:
#             author = Author.objects.get(id=author_id)
#             author.delete()
#             return Response(status=204)
#         except Author.DoesNotExist:
#             return Response({'error': 'Author not found'}, status=404)

# @api_view(['GET'])
# def get_genres(request):
#     genres = Genre.objects.all()
#     serializer = GenreSerializer(genres, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_books(request):
#     books = Book.objects.all()
#     serializer = BookSerializer(books, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_users(request):
#     users = CustomUser.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# class AuthorListCreateAPIView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = AuthorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class AuthorDetailAPIView(APIView):
#     def get_object(self, pk, format=None):
#         try:
#             author = Author.objects.get(pk=pk)
#             return author
#         except Author.DoesNotExist:
#             raise Http404("Author not found")
    
#     def get(self, request, pk):
#         author = self.get_object(pk)
#         serializer = AuthorSerializer(author)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         author = self.get_object(pk)
#         serializer = AuthorSerializer(author, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         author = self.get_object(pk)
#         author.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class GenreListCreateAPIView(APIView):
#     def get(self, request):
#         genres = Genre.objects.all()
#         serializer = GenreSerializer(genres, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = GenreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(request.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GenreDetailAPIView(APIView):
#     def get_object(self, pk):
#         try:
#             genre = Genre.objects.get(id=pk)
#             return genre
#         except Genre.DoesNotExist:
#             raise Http404("Genre doesnt found!")
        
#     def get(self, request, pk):
#         genre = self.get_object(pk)
#         serializer = GenreSerializer(genre, many=True)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         genre = self.get_object(pk=pk)
#         serializer = GenreSerializer(genre)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         genre = self.get_object(pk=pk)
#         genre.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#Authors

class AuthorListAPIView(ListAPIView):
    permission_classes = [IsStaff]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.pop('email')

        
        serializer.save()

class AuthorDeleteAPIView(APIView):
    permission_classes = [IsStaff]
    
    def get_object(self, pk):
        try:
           author = Author.objects.get(id=pk)
           return author
        except Author.DoesNotExist:
            raise Http404('Author doesn`t exist')
    
    def delete(self, request, pk):
        author = self.get_object(self, pk)
        author.delete()
        
        return Response(status=status.HTTP_404_NOT_FOUND)

class AuthorRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Books

class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookListCreateAPIView(
    UserQuerySetMixin,
    ListCreateAPIView,
):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
    ]
    # allow_staff_view = True

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        print(title)

        serializer.save(user=self.request.user)

    # def get_queryset(self, *args, **kwargs):
    #     user = self.request.user
    #     qs = super().get_queryset(*args, **kwargs)

    #     if not user.is_authenticated:
    #         return Book.objects.none()
        
    #     return qs.filter(user=user)

class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]
    permission_classes = [IsStaffOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Genres

class GenresListAPIView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericAPIView):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class GenreListAPIView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericAPIView):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class UsersListAPIView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericAPIView):
    permission_classes = [IsAdminOrReadOnlyForStaff]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        print(*args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserListAPIView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericAPIView):
    permission_classes = [IsAdminOrReadOnlyForStaff]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)