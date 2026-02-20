from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrello di {self.user}" if self.user else "Carrello"
    
    def get_total(self):
        totale=0
        for item in self.cartitem_set.all():
            totale += item.get_subtotal()
        return totale
          
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(min_value=0)

    class Meta:
        unique_together = ("cart", "product")

    def get_subtotal(self):
        return self.product.price * self.quantity