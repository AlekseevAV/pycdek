# -*- coding: utf-8 -*-
import unittest
from pycdek import Client, AbstractOrder


class TestCDEK(unittest.TestCase):
    """
    Базовые тесты для СДЭК без авторизации
    """
    def test_get_delivery_points(self):
        response = Client.get_delivery_points(44)
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

    def test_get_shipping_cost(self):
        response = Client.get_shipping_cost(44, 137, [11, 16, 137], goods=[
            {'weight': 2, 'length': 100, 'width': 10, 'height': 20}
        ])
        self.assertIsInstance(response, dict)
        self.assertIsNone(response.get('error'))


class TestCDEKClient(unittest.TestCase):
    """
    Тестирование класса Client для работы со СДЭК
    """

    # 1. Данные класса клиента для авторизации
    def test_get_user_info(self):
        client = Client(login='login', password='pswd')
        self.assertEqual(client._login, 'login')
        self.assertEqual(client._password, 'pswd')

    # 2. Выполнение запроса с неопознанным методом
    def test__exec_request(self):
        self.assertRaises(NotImplementedError, Client._exec_request, '', [], 'PUT')

    # 3. Парсинг неокрректного xml
    def test__parse_xml(self):
        parsed_xml = Client._parse_xml('<note><to>Tove</too></note>')
        self.assertIsNone(parsed_xml)


# Класс-наследник от AbstractOrder для тестирования его неабстрактных методов
class MyAbstractOrder(AbstractOrder):

    # Реализуем get_products (Возвращая None)
    def get_products(self):
        return None


class TestCDEKAbstractOrder(unittest.TestCase):
    """
    Тестирование класса AbstractOrder (через наследника MyAbstractOrder)
    """
    def setUp(self):
        self.order = MyAbstractOrder()

    # 0. Покрываем тестами свою реализацию
    def test_get_products(self):
        self.assertEqual(self.order.get_products(), None)


    # 1. Метод get_number для не заданного значения
    def test_get_number_None(self):
        self.assertRaises(AttributeError, self.order.get_number)

    # 2. Метод get_number для заданного значения
    def test_get_number_Value(self):
        self.order.number = 5
        self.assertEqual(self.order.get_number(), 5)

    # 3. Метод get_sender_name для незаданного значения
    def test_get_sender_name_Default(self):
        self.assertEqual(self.order.get_sender_name(), '')

    # 4. Метод get_sender_address для незаданного значения
    def test_get_sender_address_Default(self):
        self.assertEqual(self.order.get_sender_address(), '')

    # 5. Метод get_sender_city_id для не заданного значения
    def test_get_sender_city_id_None(self):
        self.assertRaises(AttributeError, self.order.get_sender_city_id)

    # 6. Метод get_sender_city_id для заданного значения
    def test_get_sender_city_id_Value(self):
        self.order.sender_city_id = 40
        self.assertEqual(self.order.get_sender_city_id(), 40)

    # 7. Метод get_sender_postcode для не заданного значения
    def test_get_sender_postcode_None(self):
        self.assertEqual(self.order.get_sender_postcode(), '')

    # 8. Метод get_recipient_name для не заданного значения
    def test_get_recipient_name_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_name)

    # 9. Метод get_recipient_name для заданного значения
    def test_get_recipient_name_Value(self):
        self.order.recipient_name = 'Recipient'
        self.assertEqual(self.order.get_recipient_name(), 'Recipient')

    # 10. Метод get_recipient_phone для не заданного значения
    def test_get_recipient_phone_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_phone)

    # 11. Метод get_recipient_phone для заданного значения
    def test_get_recipient_phone_Value(self):
        self.order.recipient_phone = '0000000000'
        self.assertEqual(self.order.get_recipient_phone(), '0000000000')

    # 12. Метод get_recipient_city_id для не заданного значения
    def test_get_recipient_city_id_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_city_id)

    # 13. Метод get_recipient_city_id для заданного значения
    def test_get_recipient_city_id_Value(self):
        self.order.recipient_city_id = 40
        self.assertEqual(self.order.get_recipient_city_id(), 40)

    # 14. Метод get_recipient_postcode для не заданного значения
    def test_get_recipient_postcode_None(self):
        self.assertEqual(self.order.get_recipient_postcode(), '')

    # 15. Метод get_recipient_address_street для не заданного значения
    def test_get_recipient_address_street_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_address_street)

    # 16. Метод get_recipient_address_street для заданного значения
    def test_get_recipient_address_street_Value(self):
        self.order.recipient_address_street = 'Улица'
        self.assertEqual(self.order.get_recipient_address_street(), 'Улица')

    # 17. Метод get_recipient_address_house для не заданного значения
    def test_get_recipient_address_house_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_address_house)

    # 18. Метод get_recipient_address_house для заданного значения
    def test_get_recipient_address_house_Value(self):
        self.order.recipient_address_house = '44/8'
        self.assertEqual(self.order.get_recipient_address_house(), '44/8')

    # 19. Метод get_recipient_address_flat для не заданного значения
    def test_get_recipient_address_flat_None(self):
        self.assertRaises(AttributeError, self.order.get_recipient_address_flat)

    # 20. Метод get_recipient_address_flat для заданного значения
    def test_get_recipient_address_flat_Value(self):
        # Например, рассмотрим ситуацию, когда в качестве значения выступает None
        self.order.recipient_address_flat = None
        self.assertEqual(self.order.get_recipient_address_flat(), None)

    # 21. Метод get_pvz_code для не заданного значения
    def test_get_pvz_code_None(self):
        self.assertRaises(AttributeError, self.order.get_pvz_code)

    # 22. Метод get_pvz_code для заданного значения
    def test_get_pvz_code_Value(self):
        self.order.pvz_code = '11'
        self.assertEqual(self.order.get_pvz_code(), '11')

    # 23. Метод get_shipping_tariff для не заданного значения
    def test_get_shipping_tariff_None(self):
        self.assertRaises(AttributeError, self.order.get_shipping_tariff)

    # 24. Метод get_shipping_tariff для заданного значения
    def test_get_shipping_tariff_Value(self):
        self.order.shipping_tariff = 50
        self.assertEqual(self.order.get_shipping_tariff(), 50)

    # 25. Метод get_shipping_price для не заданного значения
    def test_get_shipping_price_None(self):
        self.assertRaises(AttributeError, self.order.get_shipping_price)

    # 26. Метод get_shipping_price для заданного значения
    def test_get_shipping_price_Value(self):
        self.order.shipping_price = 140.988
        self.assertEqual(self.order.get_shipping_price(), 140.988)

    # 27. Метод get_comment для не заданного значения
    def test_get_comment_None(self):
        self.assertEqual(self.order.get_comment(), '')


if __name__ == '__main__':
    unittest.main()
