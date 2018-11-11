from django.db import models
from django.core.mail import send_mail

from core.db.timestamped import TimeStamped
from core.models import ProductPage


class BaseOrder(models.Model):

    STATUSES = (
        (1, 'Новый'),
        (2, 'В обработке'),
        (3, 'Завершен'),
        (4, 'Отменен'),
    )

    date_added = models.DateTimeField(
        verbose_name='date added',
        auto_now_add=True,
    )

    status = models.PositiveSmallIntegerField(
        verbose_name="статус",
        choices=STATUSES,
        default=1,
    )

    order_text = models.TextField(
        verbose_name="текст заказа",
        blank=True,
    )

    notified = models.BooleanField(
        default=False,
        verbose_name='уведомлён',
    )

    class Meta:
        abstract = True


class DefaultOrder(BaseOrder, TimeStamped):

    name = models.CharField(
        verbose_name="имя клиента",
        max_length=512,
    )

    phone = models.CharField(
        verbose_name="телефон",
        max_length=32,
    )

    email = models.EmailField(
        verbose_name="эл. почта",
    )

    address = models.CharField(
        verbose_name="адрес",
        max_length=512,
        blank=True,
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def save(self, *args, **kwargs):
        super(DefaultOrder, self).save(*args, **kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def total_price(self):
        return self.get_total_cost()



class OrderItem(models.Model):

    order = models.ForeignKey(
        DefaultOrder,
        related_name='items',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        ProductPage,
        related_name='order_items',
    )

    price = models.DecimalField(
        verbose_name='цена',
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=1,
    )

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    @property
    def subtotal(self):
        return self.price * self.quantity
