from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from .models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    
    subject = _('Новый заказ №{}').format(order.id)
    message = _(
        'Уважаемый(ая) {first_name},\n\n'
        'Ваш заказ №{order_id} успешно оформлен.\n'
        'Мы свяжемся с вами для уточнения деталей.\n\n'
        'Спасибо за покупку!'
    ).format(
        first_name=order.first_name,
        order_id=order.id
    )
    
    return send_mail(
        subject=subject,
        message=message,
        from_email='info@gamezone.ru',
        recipient_list=[order.email],
        fail_silently=False
    )