from django.db import models, transaction
from django.contrib.auth.models import User
from coupons.models import Coupon
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

# Create your models here.

STATUS_CHOICES=[
    ('in_attesa_pagamento', 'In attesa pagamento'),
    ('pagato', 'Pagato'),
    ('annullato', 'Annullato')
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=19, choices=STATUS_CHOICES, default='in_attesa_pagamento')
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    
    def create_from_cart(self, cart):
        if not cart.cartitem_set.exists():
            raise ValueError("Il carrello è vuoto")

        with transaction.atomic():
            if not self.pk:
                self.save()

            total = Decimal('0.00')

            for item in cart.cartitem_set.all():
                subtotal = item.product.price * item.quantity

                OrderItem.objects.create(
                    order=self,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                    subtotal=subtotal
                )

                total += subtotal

            self.total_amount = total
            self.save()
    
    def mark_as_paid(self, cart):
        if self.status == 'pagato':
            return #evita che venga eseguito di nuovo
        
        #tutto quello che sta dentro, va eseguito. Se qualcosa fallisce si annulla tutto
        with transaction.atomic():
            self.status = 'pagato'
            self.paid_at = timezone.now() #salva la data del pagamento
            self.save()

            cart.cartitem_set.all().delete() #svuota il carrello dopo l'acquisto

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
