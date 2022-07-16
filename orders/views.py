from django.urls import reverse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.admin.views.decorators import staff_member_required

from cart.carts import Cart
from orders.tasks import order_created
from orders.models import OrderItem, Order
from orders.forms import CreateOrderModelForm
from common.analizetools.analize import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


@staff_member_required
def admin_order_detail_view(request, order_id):
    order = get_object_or_404(
        klass=Order,
        pk=order_id
    )
    return render(
        request=request,
        template_name='for_admin/orders/order/detail.html',
        context={
            'order': order,
        }
    )


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
            # cart.clear()
            order_created.delay(order.pk)
            request.session['order_id'] = order.pk
            # request.session.modified = True

            # --- console ---
            console(
                request.session.items(),
                request.COOKIES,
                request.headers
            )
            # --- console ---
            cart.clear()
            return redirect(reverse(
                'payment:process'
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
