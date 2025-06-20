from rest_framework import generics

from book.models import Book
from api.serializers import BookSerializer

class BookSearchAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        result = Book.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            
            result = qs.search(q, user=user)
        
        return result