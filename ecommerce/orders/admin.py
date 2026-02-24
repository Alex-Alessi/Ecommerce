from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    fields = ["order", "product_name", "product_price", "quantity", "subtotal"]
    readonly_fields = ["subtotal"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product_name", "product_price", "quantity", "subtotal"]
    list_filter = ["product_name"]
    search_fields = ["product_name", "order__user__username"]

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    list_display = ["user", "status", "total_amount", "created_at", "paid_at"]
    list_filter = ["created_at", "status"]
    search_fields = ["user__username"]

class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["username", "email"]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# registrare un nuovo modello user, per avere UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)