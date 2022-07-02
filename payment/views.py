import braintree

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from orders.models import Order


def process_payment_view(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(
        klass=Order,
        pk=order_id
    )
    if request.method == 'POST':
        # достаём из тела post запроса токен, который сформирован js обработчиками на фронте
        nonce = request.POST.get('payment_method_nonce')

        # создание и отпрака транзакции (идентификатор платежной транзакции)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),  # - общая сумма заказа
            'payment_method_nonce': nonce,  # - token для платежной транзакции
            'options': {  # options - Дополнительные параметры
                'submit_for_settlement': True,  # - транзакция будет обрабатываться автоматически
            },
        })
        if result.is_success():
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect(to='payment:done')
        else:
            return redirect(to='payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        ctx = {
            'order': order,
            'client_token': client_token,
        }
        return render(
            request=request,
            template_name='payment/process.html',
            context=ctx
        )


def done_payment_view(request):
    return render(
        request=request,
        template_name='payment/done.html',
        context={}
    )


def canceled_payment_view(request):
    return render(
        request=request,
        template_name='payment/canceled.html',
        context={}
    )
