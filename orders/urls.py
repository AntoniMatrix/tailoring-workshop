from django.urls import path
from . import views

urlpatterns = [
    path("", views.customer_orders_page, name="customer_orders"),
    path("<int:order_id>/", views.customer_order_detail_page, name="customer_order_detail"),
]