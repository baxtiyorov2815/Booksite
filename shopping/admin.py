from django.contrib import admin
from .models import Cart, OrderItem, OrderAddress, Promotion


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered_date', 'occasion')
    search_fields = ('user__username',)
    list_filter = ('ordered_date', 'occasion')
    ordering = ('ordered_date',)
    readonly_fields = ('ordered_date', )

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'price')
    search_fields = ('book__price', 'book__title')
    readonly_fields = ('book', 'quantity', 'price')
    
@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line', 'city', 'country', 'zip_code')
    search_fields = ('user__username', 'address_line', 'city')
    
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'min_purchase_amount', 'max_discount_amount', 'is_active', 'start_date', 'end_date')
    search_fields = ('code',)
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)