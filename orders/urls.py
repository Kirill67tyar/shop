from django.urls import path

from orders.views import (
    create_order_view,
    create_order_done_view,
    admin_order_detail_view,
)

app_name = 'orders'

urlpatterns = [

    path('create-order/', create_order_view, name='create_order'),
    path('create-order/<int:order_id>/', create_order_done_view, name='create_order_done'),
    path('admin/order/', admin_order_detail_view, name='admin_order_detail'),
]
