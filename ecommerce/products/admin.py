from django.contrib import admin
from .models import Category, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "category", "is_active", "created_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["name", "description"]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
