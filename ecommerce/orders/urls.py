from django.urls import path
from . import views

urlpatterns=[
    path('', views.orders, name='ordini'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_detail/<int:pk>/', views.order_detail, name='dettaglio_ordine'),
    path('<int:pk>/paga/', views.pay_order, name='pay_order'),
]