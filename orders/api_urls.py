from django.urls import path
from . import api_views

urlpatterns = [
    # customer
    path("mine/", api_views.my_orders),
    path("create/", api_views.create_order),
    path("<int:order_id>/detail/", api_views.my_order_detail),
    path("<int:order_id>/message/", api_views.add_message_customer),

    # staff
    path("staff/list/", api_views.staff_orders),
    path("staff/<int:order_id>/detail/", api_views.staff_order_detail),
    path("staff/<int:order_id>/pricing/", api_views.staff_set_pricing),
    path("staff/<int:order_id>/status/", api_views.staff_change_status),
    path("staff/<int:order_id>/note/", api_views.staff_add_internal_note),
    path("staff/<int:order_id>/payment/", api_views.staff_add_payment),
]