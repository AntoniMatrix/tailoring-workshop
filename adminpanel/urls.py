from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="panel_dashboard"),
    path("orders/", views.orders_page, name="panel_orders"),
    path("orders/<int:order_id>/", views.order_detail_page, name="panel_order_detail"),
]