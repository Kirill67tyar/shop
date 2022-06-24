from django.urls import reverse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from cart.carts import Cart
from orders.models import OrderItem, Order
from orders.forms import CreateOrderModelForm


def create_order_view(request):
    cart = Cart(request=request)
    if request.method == 'POST':
        form = CreateOrderModelForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                )
            cart.clear()
            return redirect(reverse(
                'orders:create_order_done',
                kwargs={
                    'order_id': order.pk,
                }
            ))
    else:
        form = CreateOrderModelForm()
    return render(
        request=request,
        template_name='orders/create.html',
        context={
            'form': form,
            # 'cart': cart,
        }
    )


def create_order_done_view(request, order_id):
    order = get_object_or_404(
        klass=Order,
        pk=order_id
    )
    return render(
        request=request,
        template_name='orders/create_done.html',
        context={
            'order': order,
        }
    )
