from copy import deepcopy
from decimal import Decimal

from django.conf import settings

from store.models import Product
from coupons.models import Coupon
from common.utils import get_object_or_null


class Cart:

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})
        self.coupon_id = self.session.get('coupon_id')
        self.coupon_obj = None

    def __iter__(self):
        cart = self.cart.copy()
        # вообще, т.к. мы здесь изменяем словарь который является значением в другом словаре
        # то в теории нам нужо не просто копровать корзину, а сделать deepcopy
        # но возможно не нужно, т.к. здесь мы не вызываем метод self.save(),
        # который установит self.session.modified = True
        # тогда встаёт другой вопрос, зачем вообще тогда делать обычную копию?
        # если всё изменение зависит от self.session.modified = True
        # cart = deepcopy(self.cart)
        product_list = Product.objects.filter(pk__in=cart.keys())  # .select_related('category')

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
        # хоть словарь и изменяемый объект
        # request.session сохранится только если установить self.session.modified = True
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
        if self.session.get('coupon_id'):
            del self.session['coupon_id']
        self.save()

    @property
    def coupon(self):
        if self.coupon_id and not self.coupon_obj:
            self.coupon_obj = get_object_or_null(Coupon, pk=self.coupon_id)
        return self.coupon_obj

    def get_discount(self):
        if self.coupon:
            return self.coupon_obj.discount / Decimal('100') * self.get_full_price()
            # return self.get_full_price() / Decimal('100') * self.coupon.discount
        else:
            return Decimal('0')

    def get_full_price_after_discount(self):
        return self.get_full_price() - self.get_discount()
