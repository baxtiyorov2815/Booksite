from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()

class BookQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        
        return qs
    
class BookManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BookQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

class Author(models.Model):

    choices = (
        ('Male', 'male'),
        ('Female', 'female'),
        ('Unknown', 'unknown'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=7, choices=choices)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='media/book/author_photos', null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(
        to=CustomUser,
        default=1,
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.IntegerField()
    photo = models.ImageField(upload_to='media/book/books')
    discount = models.IntegerField(default=0, null=True, blank=True)
    sold = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True, related_name='books', verbose_name="Genre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    public = models.BooleanField(default=True)

    objects = BookManager()

    @property
    def discount_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 2)
        return self.price
    
    @property
    def average_rating(self):
        avg = self.rates.aggregate(Avg('rate'))['rate__avg']
        return round(avg, 1) if avg else 0    

    def __str__(self):
        return self.title
    
class BookRate(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_rates')
    rate = models.IntegerField(default=0)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rate}"
    
class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_comments')
    comment = models.TextField()
    rating = models.IntegerField(default=0, null=True, blank=True)
    photo = models.ImageField(upload_to='media/book/comment_photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.comment}"