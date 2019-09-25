# -*- coding: utf-8 -*-
import unittest
from pycdek3 import Client


class TestCDEKClientStatic(unittest.TestCase):
    """
    Базовые тесты для СДЭК без авторизации (статические методы класса Client)
    """
    # 0. Исходные тесты проекта:
    # Получение списка пунктов доставки в Москве (44)
    def test_get_delivery_points(self):
        response = Client.get_delivery_points(44)
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

    # Расчет стоимости доставки
    def test_get_shipping_cost(self):
        response = Client.get_shipping_cost(44, 137, [11, 16, 137], goods=[
            {'weight': 2, 'length': 100, 'width': 10, 'height': 20}
        ])
        self.assertIsInstance(response, dict)
        self.assertIsNone(response.get('error'))

    # 1. Выполнение запроса с неопознанным методом
    def test__exec_request_Method(self):
        self.assertRaises(NotImplementedError, Client._exec_request, '', [], 'PUT')

    # 2. Выполнение запроса с некорректным url
    def test__exec_request_Wrong_Url(self):
        self.assertRaises(AttributeError, Client._exec_request, None, [], 'GET')

    # 3. Выполнение запроса с некорректными данными
    def test__exec_request_Wrong_Data(self):
        self.assertRaises(AttributeError, Client._exec_request, '', None, 'GET')

    # 4. Выполнение запроса по некорректному адресу
    def test__exec_request_Error(self):
        self.assertRaises(Exception, Client._exec_request, 'http://localhost', [], 'GET')

    # 5. Парсинг неокрректного xml
    def test__parse_xml(self):
        # В данном случае используем простейший xml с ошибкой в синтаксисе
        parsed_xml = Client._parse_xml('<note><to>Tove</too></note>')
        self.assertIsNone(parsed_xml)
