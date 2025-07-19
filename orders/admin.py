from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() 
              if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response


export_to_csv.short_description = 'Export to CSV'

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'first_name', 
        'last_name', 
        'email',
        'city', 
        'paid',
        'created', 
        'updated',
        'total_cost'
    ]
    list_filter = ['paid', 'created', 'updated']
    actions = [export_to_csv]
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'city']
    list_per_page = 20

    def total_cost(self, obj):
        return obj.get_total_cost()
    total_cost.short_description = 'Общая стоимость'


admin.site.register(Order, OrderAdmin)