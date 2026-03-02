from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from coupons.models import Coupon

# Create your views here.

@login_required
def checkout(request):
    if request.method == 'GET':
        cart = request.user.cart
        cart_items = cart.cartitem_set.all()

        if not cart_items.exists():
            return redirect('carrello')

        context = {"cart":cart, "cart_items":cart_items}
        return render(request, 'checkout.html', context)
        
    if request.method == 'POST':
        cart = request.user.cart

        if not cart.cartitem_set.exists():
            return redirect('carrello')
        
        coupon_code = request.POST.get('coupon_code', None)
        coupon_obj = Coupon.objects.filter(codice=coupon_code).first()
            
        existing_order = Order.objects.filter(user=request.user,status="in_attesa_pagamento").first()
        if existing_order:
            order = existing_order
            order.coupon=coupon_obj
            order.orderitem_set.all().delete()
            order.create_from_cart(cart)
        else:
            order = Order.objects.create(user=request.user, total_amount=0, coupon = coupon_obj)
            order.create_from_cart(cart)

        return redirect('dettaglio_ordine', pk=order.pk)

        
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context={'orders':orders, }
    return render(request, 'orders/ordini.html', context)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.orderitem_set.all()

    context={'order':order, 'order_items': order_items}

    return render(request, 'orders/order_detail.html', context)

@login_required
def pay_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    cart = request.user.cart
    if order.status == "in_attesa_pagamento":
        order.mark_as_paid(cart)

    return redirect('dettaglio_ordine', pk=order.pk)