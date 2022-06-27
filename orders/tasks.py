from celery import (
    current_task,
    shared_task,
)

from django.core.mail import send_mail

from orders.models import Order
from store.utils import get_object_or_null


@shared_task
def order_created(order_id):
    order = get_object_or_null(Order, pk=order_id)
    if order:
        subject = f'Заказ № {order.pk}'
        message = f'Поздравляем, Вш заказ успешно оформлен, номер вашего заказа {order.pk}'
        mail_sent = send_mail(
            subject=subject,
            message=message,
            from_email='some_email@emal.ru',
            recipient_list=[
                order.email,
            ]
        )
        return mail_sent
    return 'Шо то не полулось'
