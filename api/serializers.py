from rest_framework import serializers
from rest_framework.reverse import reverse
from book.models import Book, Author, Genre
from accounts.models import CustomUser

from . import validators

class AuthorSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='authors_retrieve',
		lookup_field='pk',
		lookup_url_kwarg='pk'
	)
	url_edit = serializers.SerializerMethodField(
		read_only=True
	)
	class Meta:
		model = Author
		fields = ['id', 'url', 'url_edit', 'first_name', 'last_name', 'gender', 'date_of_birth', 'photo']
		read_only_fields = ['id']
		extra_kwargs = {
			'photo': {'required': False}
		}

	def get_url_edit(self, obj):
		request = self.context.get('request')
		if request is None:
			return None
		return reverse('authors_all', kwargs={'pk': obj.pk}, request=request)

	# def create(self, validated_data):
	#     email = validated_data.pop('email')
	#     obj = super().create(validated_data)
	#     print(email, obj)

	#     return obj

	# def update(self, instance, validated_data):

	#     email = validated_data.pop('email')
	#     return super().update(instance, validated_data)

class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['id', 'title']
		read_only_fields = ['id']

class BookSerializer(serializers.ModelSerializer):

	title = serializers.CharField(validators=[validators.unique_validator_title, validators.validate_title_no_hello])

	class Meta:
		model = Book
		fields = [
			#'user',
			'id', 
			'title', 
			'description', 
			'price', 
			'amount', 
			'photo', 
			'discount', 
			'sold', 
			'is_active', 
			'author', 
			'genres', 
			'created_at', 
			'updated_at', 
			'discount_price', 
			'average_rating'
			]
		read_only_fields = ['id', 'created_at', 'updated_at', 'discount_price', 'average_rating']
		extra_kwargs = {
			'photo': {'required': False}
		}

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
		read_only_fields = ['id', 'is_active']
		extra_kwargs = {
			'email': {'required': True},
			'first_name': {'required': False},
			'last_name': {'required': False}
		}