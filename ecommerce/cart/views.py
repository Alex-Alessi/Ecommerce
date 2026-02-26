from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

# Create your views here.

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

    if not created:
        cart_item.quantity +=1
        cart_item.save()

    return redirect('catalogo')

@login_required
def cart_detail(request):
    try:
        cart = request.user.cart
        items = cart.cartitem_set.all()
        total = cart.get_total()
    except Cart.DoesNotExist:
        items = []
        total = 0

    context={"items":items, "total": total}
    return render(request, 'cart/carrello.html', context)

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carrello')

