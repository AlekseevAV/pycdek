# -*- coding: utf-8 -*-
from pycdek3 import AbstractOrder, AbstractOrderLine


class MyOrder(AbstractOrder):
    """
    Класс-наследник от AbstractOrder для тестирования
    """
    def __init__(self, id_value=1, lines=None):
        self.id = id_value
        self.lines = lines

    # Список товаров в заказе
    def get_products(self):
        return self.lines


class MyOrderLine(AbstractOrderLine):
    """
    Класс-наследник от AbstractOrderLine для тестирования
    """
    product = {
        'title': 'Шлакоблок',
        'weight': 1000,
        'price': 500,
        'id': 1
    }

    def __init__(self, order=None):
        self.parent_order = order

    def get_product_title(self):
        return self.product['title']

    def get_product_upc(self):
        return self.product['id']

    def get_product_weight(self):
        return self.product['weight']

    def get_product_price(self):
        return self.product['price']

    def get_product_payment(self):
        if self.parent_order and self.parent_order.is_paid:
            return 0
        else:
            return self.product['price']  # оплата при получении
