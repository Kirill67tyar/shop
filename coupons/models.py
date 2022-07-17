from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Код купона'

    )
    valid_from = models.DateTimeField(
        verbose_name='Активен с какого числа'
    )
    valid_to = models.DateTimeField(
        verbose_name='Активен до какого числа'
    )
    discount = models.IntegerField(
        validators=(
            MinValueValidator(1),  # валидация этих полей происзодит на уровне Django а не базы данных
            MaxValueValidator(100)
        ),
        verbose_name='Скидка'
    )
    active = models.BooleanField(
        default=False,
        verbose_name='Активен',
    )

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return f'{self.code} (active - {self.active}, discount - {self.discount}%)'
