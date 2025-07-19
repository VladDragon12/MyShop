from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
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

export_to_csv.short_description = "Export selected orders to CSV"


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                'admin/orders/order/detail.html',
                {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # очистка корзины
            cart.clear()
            order_created.delay(order.id)  # Вызываем задачу с delay()
            
            return render(
                request,
                'orders/order/created.html',
                {'order': order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )


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
        'coupon',
        'discount'
    ]
    list_filter = ['paid', 'created', 'updated']
    actions = [export_to_csv]
    search_fields = ['first_name', 'last_name', 'email', 'city']
    list_per_page = 20

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [
            path('<int:order_id>/detail/',
                 self.admin_site.admin_view(admin_order_detail),
                 name='order_detail'),
        ]
        return my_urls + urls