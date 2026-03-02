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
            return redirect('dettaglio_ordine', pk=order.pk)
    
    except Cart.DoesNotExist:
        return redirect('carrello')
    
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
    order.mark_as_paid(cart)

    return redirect('dettaglio_ordine', pk=order.pk)