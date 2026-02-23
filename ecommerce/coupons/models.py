from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Coupon(models.Model):
    codice = models.CharField(max_length=100, unique=True)
    percentuale = models.PositiveIntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1) 
        ])
    is_active = models.BooleanField(default=False)
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_scadenza = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.codice
    
    def is_valid(self):
        if not self.is_active:
            return False
        elif self.data_scadenza and self.data_scadenza < timezone.now():
            return False
        return True