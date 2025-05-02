from django.db import models
from accounts.models import CustomUser
from book.models import Book
from django.utils import timezone
    
class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"OrderItem {self.id} for {self.book.title}"

class Cart(models.Model):
    choices = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField('OrderItem', blank=True, related_name='order_items')
    occasion = models.CharField(max_length=100, blank=True, choices=choices, default='Pending')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_ordered = models.BooleanField(default=False)
    badge = models.CharField(max_length=100, blank=True, choices=choices, default='light')
    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
    
class OrderAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100, blank=True)
    is_visible = models.BooleanField(default=True)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Address for {self.user.username}"
    
class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    used = models.IntegerField(default=0)
    null_shipping = models.BooleanField(default=False)
    max_uses = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Promotion {self.code}"