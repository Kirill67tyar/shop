from django.shortcuts import render, get_object_or_404, HttpResponse

from store.utils import get_object_or_null
from store.models import Product, Category

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
    # console(request.headers)
    # p_dir(request)
    console(request.session, sdict=True)
    console_compose(request.session)
    # --- console ---

    return render(
        request=request,
        template_name='store/product/list.html',
        context=ctx
    )


def detail_product_view(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    return render(
        request=request,
        template_name='store/product/detail.html',
        context={
            'product': product,
        }
    )
