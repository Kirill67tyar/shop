from copy import deepcopy
from decimal import Decimal

from django.conf import settings

from store.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.setdefault(settings.CART_SESSION_ID, {})
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        # cart = deepcopy(self.cart)
        product_list = Product.objects.filter(pk__in=cart.keys())

        for product in product_list:
            cart[str(product.pk)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # return sum(list(map(lambda x: x['quantity'], self.cart.values())))
        return sum([item['quantity'] for item in self.cart.values()])

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.pk)
        self.cart.setdefault(
            product_id,
            {
                'quantity': 0,
                'price': str(product.price),
            }
        )
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_full_price(self):
        return sum(
            [Decimal(item['price']) * item['quantity']
             for item in self.cart.values()]
        )

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
