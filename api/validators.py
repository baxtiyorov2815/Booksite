from rest_framework import serializers
from book.models import Book
from rest_framework.validators import UniqueValidator
# def validate_title(value):
#     qs = Book.objects.filter(title__iexact=value)
#     if qs.exists():
#         raise serializers.ValidationError(
#             f"{value} already exists!"
#         )
	
#     return value

def validate_title_no_hello(value):
	if 'hello' in value.lower():
		raise serializers.ValidationError(f"{value} not allowed")
	
	return value

unique_validator_title = UniqueValidator(queryset=Book.objects.all(), lookup='iexact')