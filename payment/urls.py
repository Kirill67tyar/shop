from django.urls import path

from payment.views import (
    process_payment_view,
    done_payment_view,
    canceled_payment_view,
)

app_name = 'payment'

urlpatterns = [
    path('process/', process_payment_view, name='process'),
    path('done/', done_payment_view, name='done'),
    path('canceled/', canceled_payment_view, name='canceled'),
]
