from django.contrib import admin

from store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug',
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'slug', 'category', 'available', 'price', 'created', 'updated',
    list_editable = 'available', 'price',
    list_filter = 'category', 'available', 'created', 'updated',
    prepopulated_fields = {'slug': ('name',)}


"""
category
    name
    slug
    photo
    description
    available
    price
    created
    updated
"""
