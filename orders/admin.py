import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem

from common.analizetools.analize import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


# -------- export to csv ---------
def export_to_csv(modeladmin, request, queryset):
    # достаём метаданные нашей модели (класс Options)
    opts = modeladmin.model._meta

    # создаём response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment;filename={opts.verbose_name}.csv'

    # создаём объект для записи csv
    writer = csv.writer(response)
    # делаем заголовки
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # записываем заголовки
    writer.writerow(
        [field.verbose_name for field in fields]
    )

    # записываем содержимое
    for item in queryset:
        row_data = []
        for field in fields:
            cell = getattr(item, field.name)
            if isinstance(cell, datetime.datetime):
                cell = cell.strftime(format='%d/%m/%Y/')
            row_data.append(cell)
        writer.writerow(row_data)

    # --- console ---
    delimiter(sym=' - ')
    print(response)
    delimiter(sym=' - ')
    console_compose(response)
    # --- console ---

    return response


# добавляем как действие будет отображаться на сайте администрирования
export_to_csv.short_description = 'Экспортировать в файл CSV'  # 'Export to CSV'


# -------- export to csv ---------


def order_detail(obj):
    url = reverse_lazy('orders:admin_order_detail', args=[obj.pk, ])
    return mark_safe(f'<a href={url}>View</a>')


def order_pdf(obj):
    url = reverse_lazy('orders:admin_order_pdf', args=[obj.pk, ])
    return mark_safe(f'<a href={url}>PDF</a>')


order_pdf.short_description = 'Счёт'


class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = 'product',


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'first_name', 'email', 'city',
        'created', 'updated', 'paid',
        order_detail, order_pdf,
    )
    list_filter = ('paid', 'created', 'updated',)
    inlines = (OrderItemTabularInline,)
    actions = [export_to_csv, ]
