from django import forms

from orders.models import Order


class CreateOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email',
            'postal_code', 'city', 'address',
        )
