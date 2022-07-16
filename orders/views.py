from wkhtmltopdf.views import PDFTemplateView

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


class MyPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'my_template.html'
    cmd_options = {
        'margin-top': 3,
    }

    # def get(self, request, order_id=None, *args, **kwargs):
    #     user = request.user
    #     if order_id and user.is_authenticated and user.is_active and user.is_staff:
    #         order = get_object_or_404(
    #             klass=Order,
    #             pk=order_id
    #         )
    #         self.template_name = render_to_string(
    #             template_name='orders/to_pdf.html',
    #             context={
    #                 'order': order,
    #             }
    #         )
    #         self.filename = f'order_{order_id}.pdf'
    #         super().get(request, order_id=None, *args, **kwargs)
    #     else:
    #         return HttpResponse(status=403)

    def get_filename(self):
        request = self.request
        user = request.user
        order_id = request.get_full_path_info().split('/')[-3]
        if order_id and user.is_authenticated and user.is_active and user.is_staff:
            order = get_object_or_404(
                klass=Order,
                pk=order_id
            )
            self.template_name = render_to_string(
                template_name='orders/to_pdf.html',
                context={
                    'order': order,
                }
            )
            self.filename = f'order_{order_id}.pdf'
        return self.filename


@staff_member_required
def admin_order_pdf_view(request, order_id):
    order = get_object_or_404(
        klass=Order,
        pk=order_id
    )
    html = render_to_string(
        template_name='orders/to_pdf.html',
        context={
            'order': order,
        }
    )

    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(html)
    content = pdf.output(name=f'order_{order.pk}.pdf', dest='S').encode('latin-1')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    response.write(content=content)
    return response
