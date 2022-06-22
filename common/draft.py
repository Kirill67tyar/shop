# from django.contrib.sessions.backends.db import SessionStore
# from django.conf import settings

class Cart:

    def __init__(self, request, *args, **kwargs):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # ключами в словаре self.cart будет id товаров,
        # а значением - другой словарь с ключами количества и цена {'quantity':..., 'price':...,}

        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """добавляет продукт в корзину или обновляет его кол-во"""
        # product - экземпляр класса модели Product
        # почему str? ключом в JSON может быть только string
        product_id = str(product.pk)
        item = {'quantity': 0, 'price': str(product.price), }

        # проверяем есть ли у нас ключ product_id. если нет, то создаем новый:
        self.cart[product_id] = self.cart.get(product_id, item)

        # если update_quantity == True - то присваиваем новую цену
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        # иначе добавляем
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # modified (по умолчанию False) - позволит подтвердить наши изменения
        self.session.modified = True

    def remove(self, product, minus_one=False):
        """
        Удаляем товар из корзины по одному, если update_quantity=True, или полностью
        """
        product_id = str(product.pk)
        if product_id in self.cart:
            # if minus_one and self.cart[product_id]['quantity'] > 1:
            #     self.cart[product_id]['quantity'] -= 1
            # else:
            #     del self.cart[product_id]
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Проходим по товарам корзины и получаем словари объекты словарь, со значениями:
        quantity: количество данного товара (тип данных int)
        product: объект класса Product
        price: price - экземпляр класса Price
        total_price: итоговая цена (цена одного экземпляра умноженное на количество)
        """
        cart = self.cart.copy()
        products = Product.objects.filter(id__in=cart.keys())

        # добавляем в наш словарь (значчения ключа product_id) экземпляр модели Product
        for product in products:
            cart[str(product.pk)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Получение итогового количества товаров"""
        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price(self):
        """Получение итоговой цена"""
        return sum([Decimal(item['price']) * item['quantity'] for item in self.cart.values()])

    def clear(self):
        """Очищение корзины"""
        del self.session[settings.CART_SESSION_ID]
        if self.session.get('coupon_id'):
            del self.session['coupon_id']
        self.save()