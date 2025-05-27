from rest_framework.serializers import ModelSerializer
from book.models import Book, Author, Genre
from accounts.models import CustomUser

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'photo']
        read_only_fields = ['id']
        extra_kwargs = {
            'photo': {'required': False}
        }

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']
        read_only_fields = ['id']

class BookSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'price', 'amount', 'photo', 'discount', 'sold', 'is_active', 
                  'author', 'genres', 'created_at', 'updated_at', 'discount_price', 'average_rating']
        read_only_fields = ['id', 'created_at', 'updated_at', 'discount_price', 'average_rating']
        extra_kwargs = {
            'photo': {'required': False}
        }

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'is_active']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }