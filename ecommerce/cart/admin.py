from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ["product", "quantity", "subtotal_display"]
    readonly_fields = ["subtotal_display"]

    def subtotal_display(self, obj):
        return obj.get_subtotal()
    subtotal_display.short_description = "Subtotal"

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ["user", "created_at", "updated_at"]
    list_filter = ["updated_at"]
    search_fields = ["user.username"]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity", "subtotal_display"]
    list_filter = ["product"]
    search_fields = ["product__name", "cart__user__username"]

    def subtotal_display(self, obj):
        return obj.get_subtotal()  # metodo del modello
    subtotal_display.short_description = "Subtotal"  # titolo colonna

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)