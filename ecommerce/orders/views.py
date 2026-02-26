from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

# Create your views here.

@login_required
def checkout(request):
    try:
        cart = request.user.cart
        if not cart.cartitem_set.exists():
            return redirect('carrello')
        else:
            order = Order.objects.create(user=request.user, total_amount=0)
            order.create_from_cart(cart)
            order.mark_as_paid(cart)
            return redirect('catalogo')
    
    except Cart.DoesNotExist:
        return redirect('carrello')
    

