from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, HttpResponse

from store.recommenders import Recommender
from store.models import Product, Category

from cart.forms import AddToCartForm
from common.analizetools.analize import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


def list_product_view(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    ctx = {
        'categories': categories,
        'category': category,
        'products': products,
    }

    # --- console ---
    console_compose(
        request,
        sdir=False
    )
    # --- console ---

    return render(
        request=request,
        template_name='store/product/list.html',
        context=ctx
    )


def detail_product_view(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    cart_form = AddToCartForm()
    r = Recommender()
    recommendations = r.suggest_products_for(
        products=[product],
        max_length=4
    )
    return render(
        request=request,
        template_name='store/product/detail.html',
        context={
            'product': product,
            'cart_form': cart_form,
            'recommendations': recommendations,
        }
    )


def experiment_view(request):
    msg = EmailMultiAlternatives(
        subject='проверка',
        body='ПРОВЕРКА',
        from_email=settings.EMAIL_HOST_USER,
        to=['kirillbogomolov.ric@gmail.com', ]
    )
    msg.send()
    response = HttpResponse()
    # --- console ---
    # console(response.headers)
    # # console(request.headers)
    # # p_dir(request)
    # # console(request.session, sdict=True)
    # # console(request.COOKIES)
    # # console_compose(request.session)
    # console(request.get_full_path_info().split('/'))

    # --- console ---
    return JsonResponse({'status': 'ok', })
