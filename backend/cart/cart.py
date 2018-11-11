from decimal import Decimal

from django.conf import settings

from core.models import ProductPage


class CartItem(object):
    """
    Ассоциированный с ProductPage элемент с количеством и ценой
    """

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = int(quantity)
        self.price = Decimal(str(price))

    def __repr__(self):
        return "CartItem Object {0}".format(self.product)

    def to_dict(self):
        return {
            'product_pk': self.product.pk,
            'quantity': self.quantity,
            'price': str(self.price),
        }

    @property
    def subtotal(self):
        """
        Промежуточная сумма по всем товарам элемента
        """
        return self.price * self.quantity


class Cart(object):
    """
    Session-based корзина товаров
    """

    def __init__(self, session, session_key='CART'):
        self._items_dict = {}
        self.session = session
        self.session_key = session_key

        if self.session_key in self.session:
            cart_represenation = self.session[self.session_key]
            ids_in_cart = cart_represenation.keys()
            products_queryset = ProductPage.objects.filter(id__in=ids_in_cart)
            for product in products_queryset:
                item = cart_represenation[str(product.pk)]
                self._items_dict[product.pk] = CartItem(
                    product,
                    item['quantity'],
                    Decimal(item['price']),
                )

    def __contains__(self, product):
        """
        Проверка вхождения ProductPage в корзину
        """
        return product in self.products

    def update_session(self):
        """
        Обновление ассоциированной сессии пользователя
        """
        self.session[self.session_key] = self.cart_serializable
        self.session.modified = True

    def add(self, product, price=None, quantity=1):
        """
        Добавление продукта в корзину
        Для существующего продукта количество увеличивается
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Мин кол-во товаров должно быть не меньше 1')
        if product in self.products:
            self._items_dict[product.pk].quantity += quantity
        else:
            if price is None:
                raise ValueError('Отсутсвует цена добавляемого товара')
            self._items_dict[product.pk] = CartItem(product, quantity, price)
        self.update_session()

    def remove(self, product):
        """
        Удаление товара из корзины
        """
        if product in self.products:
            del self._items_dict[product.pk]
            self.update_session()

    def clear(self):
        """
        Очистка корзины
        """
        self._items_dict = {}
        self.update_session()

    def set_quantity(self, product, quantity):
        """
        Изменение значения количества единиц товара в корзине
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError(
                'Количество товаров должно быть целым позитивным числом')
        if product in self.products:
            self._items_dict[product.pk].quantity = quantity
            if self._items_dict[product.pk].quantity < 1:
                del self._items_dict[product.pk]
            self.update_session()

    @property
    def items(self):
        """
        Список позиций в корзине
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        Сериализуемое представление корзины
        Пример:
        {
            '1': {'product_pk': 1, 'quantity': 2, price: '9.99'},
            '2': {'product_pk': 2, 'quantity': 3, price: '29.99'},
        }
        """
        cart_represenation = {}
        for item in self.items:
            product_id = str(item.product.pk)
            cart_represenation[product_id] = item.to_dict()
        return cart_represenation

    @property
    def items_serializable(self):
        """
        Список позиций, форматированный для сериализации
        """
        return self.cart_serializable.items()

    @property
    def count(self):
        """
        Число товаров в корзине (общая сумма)
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        Число уникальных позиций в корзине
        """
        return len(self._items_dict)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def products(self):
        """
        Список ассоциированных товаров
        """
        return [item.product for item in self.items]

    @property
    def total_price(self):
        """
        Общая сумма товаров в корзине
        """
        return sum(item.subtotal for item in self.items)
