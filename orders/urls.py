from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'orders'

urlpatterns = [
    path(_('create/'), views.order_create, name='order_create'),
    path(_('admin/order/') + '<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]