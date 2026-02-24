from django.contrib import admin
from .models import Coupon

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["codice", "percentuale", "is_active", "data_creazione", "data_scadenza"]
    list_filter = ["is_active", "data_scadenza"]
    search_fields = ["codice"]

admin.site.register(Coupon, ProductAdmin)