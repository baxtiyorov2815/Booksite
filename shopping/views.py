from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, OrderItem, OrderAddress, Promotion
from book.models import Book
from django.contrib import messages


class CartView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass

class AddItemToCartView(View):
    def post(self, request, pk):
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
        except ValueError:
            messages.add_message(request, messages.ERROR, "Invalid amount")
            return redirect('book_detail', pk)
        book = Book.objects.get(pk=pk)
        cart = Cart.objects.get_or_create(user=request.user)[0]
        order_item, created = OrderItem.objects.get_or_create(book=book)
        cart.items.add(order_item)
        cart.save()
        if book.amount < amount:
            messages.add_message(request, messages.ERROR, "Not enough stock available")
            return redirect('book_detail', pk)
        if created:
            order_item.quantity = amount
            order_item.price = book.price * amount
            order_item.save()
        else:
            order_item.quantity += amount
            order_item.price += book.price * amount
            order_item.save()
        messages.add_message(request, messages.SUCCESS, "Item added to cart")
        return redirect('home')
    
class RemoveItemFromCartView(View):
    def post(self, request, pk):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        order_item = OrderItem.objects.get(pk=pk)
        order_item.delete()
        messages.add_message(request, messages.SUCCESS, "Item removed from cart")
        return redirect('home')
    
class CheckoutView(View):
    shipping_cost = 14.00
    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        if not cart.items.exists() or cart.is_ordered:
            messages.add_message(request, messages.ERROR, "No items in cart")
            return redirect('home')

        user = request.user
        adresses = OrderAddress.objects.filter(user=user, is_visible=True)
        order_items = cart.items.all()
        if not order_items.exists():
            messages.add_message(request, messages.ERROR, "No items in cart")
            return redirect('home')
        total_price = sum(item.price for item in order_items)
        discount = 0
        for item in order_items:
            if item.book.discount:
                discount += (item.book.discount * item.price) / 100
        total_cost = float(total_price) + self.shipping_cost - float(discount)
        if request.GET.get('promo_code'):
            promo_code = request.GET.get('promo_code')
            try:
                promotion = Promotion.objects.get(code=promo_code, is_active=True)
                if promotion.null_shipping:
                    self.shipping_cost = 0.00
                    total_cost -= 14.00
                    messages.add_message(request, messages.SUCCESS, "Shipping cost waived!")
                if total_price >= promotion.min_purchase_amount:
                    promo_discount = (total_price * promotion.discount_percentage) / 100
                    if promotion.max_discount_amount and discount > promotion.max_discount_amount:
                        promo_discount = promotion.max_discount_amount
                    total_cost -= float(promo_discount)
                    cart.total_price = total_cost
                    cart.save()
                    promotion.used += 1
                    messages.add_message(request, messages.SUCCESS, f"Promo code applied! Discount: {promo_discount}")
                else:
                    messages.add_message(request, messages.ERROR, "Minimum purchase amount not met")
            except Promotion.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Invalid promo code")
        return render(request=request, 
                      template_name='book/checkout.html', 
                      context={'order_items': order_items, 
                               'adresses': adresses, 
                               'total_price': total_price, 
                               'discount': discount, 
                               'shipping_cost': self.shipping_cost, 
                               'total_cost': total_cost
                               }
                               )
    
    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        order_items = cart.items.all()
        address_id = request.POST.get('shipping_addres')
        if address_id:
            address = OrderAddress.objects.get(pk=address_id)
        elif request.POST.get('address_line'):
            try:
                address = OrderAddress.objects.create(
                    user=request.user,
                    address_line=request.POST.get('address_line'),
                    city=request.POST.get('city'),
                    house_number=request.POST.get('house_number'),
                    country=request.POST.get('country'),
                    zip_code=request.POST.get('zip_code')
                )
                if request.POST.get('save'):
                    address.is_visible = True
                else:
                    address.is_visible = False
                address.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Invalid address details")
                return redirect('checkout')
        else:
            messages.add_message(request, messages.ERROR, "No address provided")
            return redirect('checkout')
        for item in order_items:
            item.order = cart
            item.save()
        cart.occasion = "Pending"
        cart.is_ordered = True
        cart.save()
        messages.add_message(request, messages.SUCCESS, "Order placed successfully")
        return redirect('home')
    
class WishlistView(View):
    def get(self, request):
        try:
            carts = Cart.objects.filter(user=request.user, is_ordered=True)
            order_items = [items for item in carts for items in item.items.all()]
            price = sum(item.price for item in order_items)
            for cart in carts:
                if cart.occasion == "Pending":
                    cart.badge = "info"
                elif cart.occasion == "Shipped":
                    cart.badge = "warning"
                elif cart.occasion == "Delivered":
                    cart.badge = "success"
                elif cart.occasion == "Cancelled":
                    cart.badge = "danger"
                cart.save()
            return render(request=request, 
                        template_name='book/wishlist.html', 
                        context={'carts': carts, 
                                'price': price,
                                }
                                )
        except Cart.DoesNotExist:
            messages.add_message(request, messages.ERROR, "No items in wishlist")
            return redirect('home')
    def post(self, request):
        id = request.POST.get('cart_id')
        try:
            cart = Cart.objects.get(pk=id)
            cart.delete()
            messages.add_message(request, messages.SUCCESS, "Item removed from wishlist")
            return redirect('wishlist')
        except Cart.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Item not found")
            return redirect('wishlist')