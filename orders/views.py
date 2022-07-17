import os
import pdfkit

from django.conf import settings
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

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
        template_name='admin/orders/order/detail.html',
        context={
            'order': order,
        }
    )


def create_order_view(request):
    cart = Cart(request=request)
    if request.method == 'POST':
        form = CreateOrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=True)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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


# # вариант который не работает, т.к. для weasyprint нужен windows 11
# @staff_member_required
# def admin_order_pdf_view(request, order_id):
#     order = get_object_or_404(
#         klass=Order,
#         pk=order_id
#     )
#     html = render_to_string(
#         template_name='orders/to_pdf.html',
#         context={
#             'order': order,
#         }
#     )
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
#     weasyprint.HTML(string=html).write_pdf(
#         response,
#         stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
#     )
#     return response

# вполне себе рабочий кошерный вариант.
# используется программа - wkhtmltopdf
# и библиотека pdfkit
# https://pypi.org/project/pdfkit/
# https://www.javatpoint.com/converting-html-to-pdf-files-using-python
@staff_member_required
def admin_order_pdf_view(request, order_id):
    order = get_object_or_404(
        klass=Order,
        pk=order_id
    )

    html_string = render_to_string(
        template_name='orders/to_pdf.html',
        context={
            'order': order,
        }
    )

    # storing string to pdf file
    content = pdfkit.from_string(
        input=html_string,
        output_path=False,
        css='static/css/pdf.css',
        configuration=settings.WKHTMLTOPDF_CONFIG
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    response.write(content=content)
    return response
