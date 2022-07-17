from django.http import JsonResponse, HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views.decorators.http import require_POST

from store.models import Product
from cart.carts import Cart
from cart.forms import AddToCartForm
from coupons.forms import CouponApplyForm

from common.analizetools.analize import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


@require_POST
def add_to_cart_view(request, product_id):
    cart = Cart(request=request)
    product = get_object_or_404(
        klass=Product,
        pk=product_id
    )
    form = AddToCartForm(data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update'],
        )
    return redirect(to='cart:detail_cart')


def remove_from_cart_view(request, product_id):
    cart = Cart(request=request)
    product = get_object_or_404(
        klass=Product,
        pk=product_id
    )
    cart.remove(product)
    return redirect(to='cart:detail_cart')


def detail_cart_view(request):
    cart = Cart(request=request)
    for item in cart:
        item['update_quantity_form'] = AddToCartForm(
            initial={
                'quantity': item['quantity'],
                'update': True,
            }
        )
    if cart.coupon:
        coupon_apply_form = CouponApplyForm(
            initial={
                'code': cart.coupon.code,
            }
        )
    else:
        coupon_apply_form = CouponApplyForm()
    return render(
        request=request,
        template_name='cart/detail.html',
        context={
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
        }
    )


def experiment(request):
    cart = Cart(request)

    # --- console ---
    console(request.COOKIES)
    # console(request.META)
    # p_dir(request)
    # console(HttpResponse().headers)
    # --- console ---

    return JsonResponse({'status': 'ok'})
