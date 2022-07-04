import braintree

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from orders.models import Order
from common.analizetools.analize import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


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
        # причём передача в метод sale делает скорее всего HTTP запрос
        # т.е. строка ниже делает HTTP запрос, совершает снятие денег со счёта
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost),  # - общая сумма заказа
            'payment_method_nonce': nonce,  # - token для платежной транзакции
            'options': {  # options - Дополнительные параметры
                'submit_for_settlement': True,  # - транзакция будет обрабатываться автоматически
            },
        })
        # если снятие со счёта прошло успешно (is_success)
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id

            # --- console ---
            console(
                request.session,
                request.COOKIES,
                request.headers,
            )
            # --- console ---

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
