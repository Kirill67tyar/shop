from django.urls import path

from cart.views import (
    add_to_cart_view,
    detail_cart_view,
    remove_from_cart_view,
    experiment
)

app_name = 'cart'

urlpatterns = [
    path('', detail_cart_view, name='detail_cart'),
    path('add/<int:product_id>', add_to_cart_view, name='add_to_cart'),
    path('remove/<int:product_id>', remove_from_cart_view, name='remove_from_cart'),
    path('experiment/', experiment, name='experiment'),
]
