from django.urls import path
from . import views

urlpatterns=[
    path('carrello', views.cart_detail, name="carrello")
]