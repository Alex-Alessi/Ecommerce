from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='prodotti/foto/', null=True, blank=True)
#     is_primary = models.BooleanField(default=False)

#     class Meta:
#         ordering = ['-is_primary']

#     def __str__(self):
#         return f"Foto di {self.product}"
