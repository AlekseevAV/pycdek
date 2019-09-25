# -*- coding: utf-8 -*-
import unittest
from tests.helpers import MyOrderLine, MyOrder


class TestCDEKAbstractOrderLine(unittest.TestCase):
    """
    Тестирование класса AbstractOrderLine (через наследника MyAbstractOrderLine)
    """
    def setUp(self):
        self.order_line = MyOrderLine()
        self.order = MyOrder()
        self.order.is_paid = True

    # 0. Покрываем тестами свою реализацию
    def test_get_product_upc(self):
        self.assertEqual(self.order_line.get_product_upc(), 1)

    def test_get_product_weight(self):
        self.assertEqual(self.order_line.get_product_weight(), 1000)

    def test_get_product_price(self):
        self.assertEqual(self.order_line.get_product_price(), 500)

    # Стоимость при неоплаченном заказе/отсутствии заказа
    def test_get_product_payment_Product(self):
        self.assertEqual(self.order_line.get_product_payment(), 500)

    # Стоимость при оплаченном заказе
    def test_get_product_payment_Parent(self):
        self.order_line.parent_order = self.order
        self.assertEqual(self.order_line.get_product_payment(), 0)

    def test_get_product_title(self):
        self.assertEqual(self.order_line.get_product_title(), 'Шлакоблок')

    # 1. Метод get_quantity для не заданного значения
    def test_get_quantity_None(self):
        self.assertRaises(AttributeError, self.order_line.get_quantity)

    # 2. Метод get_quantity для заданного значения
    def test_get_quantity_Value(self):
        self.order_line.quantity = 5
        self.assertEqual(self.order_line.get_quantity(), 5)
