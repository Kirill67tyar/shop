from django.urls import path

from store.views import (
    list_product_view,
    detail_product_view,
)

app_name = 'store'

urlpatterns = [
    path('', list_product_view, name='list_products'),
    path('<slug:category_slug>/', list_product_view, name='list_products_by_category'),
    path('<int:pk>/<slug:slug>/', detail_product_view, name='detail_product'),
]
