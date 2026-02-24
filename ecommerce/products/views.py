from django.shortcuts import render
from .models import Category, Product

# Create your views here.

def catalogo(request):
    prodotti = Product.objects.filter(is_active=True).order_by('-created_at')

    context={"prodotti": prodotti}

    return render(request, 'products/catalogo.html', context)