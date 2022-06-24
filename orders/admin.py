from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = 'product',


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'first_name', 'last_name',
        'email', 'postal_code', 'city',
        'address', 'created', 'updated', 'paid',
    )
    list_filter = ('paid', 'created', 'updated',)
    inlines = (OrderItemTabularInline,)


"""
first_name
    last_name
    email
    postal_code
    city
    created
    updated
    paid
"""
