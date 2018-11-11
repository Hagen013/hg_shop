from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from celery.decorators import periodic_task
from config.celery import app

from .models import DefaultOrder, OrderItem


@periodic_task(run_every=timedelta(seconds=60))
def mail_queue():
    print("Task is executed every minute")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
@transaction.non_atomic_requests
def UserOrderNotification(order_pk):
    """
    Отправка пользователю уведомления об
    успешном оформлении заказа
    """
    subject = 'ТОРГОСВЕТ: заказ c номером {}'.format(order_pk)
    order = DefaultOrder.objects.get(id=order_pk)

    message = 'ТОРГОСВЕТ: Номер Вашего заказа: {0}\nВ течение рабочих суток вам позвонит сотрудник для уточнения деталей заказа\nЕсли это письмо адресовано не Вам, мы просим извинения'.format(order_pk)
    mail_send = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_send


@app.task
@transaction.non_atomic_requests
def AdminOrderNotification(order_pk):
    """
    Отправка администратору уведомления о
    поступлении заказа
    """
    order = DefaultOrder.objects.get(id=order_pk)
    order_items = OrderItem.objects.filter(order__pk=order_pk)

    text = '\nID ЗАКАЗА: {0}; СУММА: {1} рублей\n'.format(order.id, order.get_total_cost())
    line = 'ОТ: {0}\nТелефон: {1}, Почта: {2}\nГород: {3}\nПримечания:{4}'.format(
        order.name,
        order.phone,
        order.email,
        order.address,
        order.order_text
    )
    text += line
    for item in order_items:
        line = '\nАртикул: {0}, кол-во:{1}, сумма:{2} руб.,\nнаименование:{3}\n'.format(
            item.product.vendor_code,
            item.quantity,
            item.subtotal,
            item.product.name,
        )
        text += line

    subject = 'Заказ №{0}'.format(order.id)
    mail_send = send_mail(subject, text, settings.EMAIL_HOST_USER, [settings.EMAILS_ADMIN])
    return mail_send
