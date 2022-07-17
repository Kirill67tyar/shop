from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия'
    )
    email = models.EmailField()
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес'
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='Почтовый индекс'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обнавлён'
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Уплачено'
    )
    braintree_id = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='ID чека'
    )
    coupon = models.ForeignKey(
        to='coupons.Coupon',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders',
        verbose_name='Купон'
    )
    discount = models.IntegerField(
        default=0,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name='Скидка'
    )

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ: {self.pk} | Дата: {self.created} | Заказчик: {self.email}'

    # @property
    # def get_total_cost(self):
    #     return sum(item.get_cost for item in self.items.all())

    @property
    def get_total_cost(self):
        total_cost = sum(item['price'] * item['quantity'] for item in self.items.values('price', 'quantity'))
        return total_cost - total_cost * (self.discount / Decimal('100'))

    @property
    def get_total_cost_without_discount(self):
        return sum(item['price'] * item['quantity'] for item in self.items.values('price', 'quantity'))


class OrderItem(models.Model):
    order = models.ForeignKey(
        to='Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        to='store.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    class Meta:
        ordering = ('-price',)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cost(self):
        return self.quantity * self.price
