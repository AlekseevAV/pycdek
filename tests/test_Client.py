# -*- coding: utf-8 -*-
import unittest
import datetime
from xml.etree import ElementTree

from pycdek3 import Client
from tests.helpers import MyOrder, MyOrderLine


class TestClient(Client):
    """
    Переопределенный класс для замены API url для тестирования
    """
    INTEGRATOR_URL = 'https://integration.edu.cdek.ru'
    CREATE_ORDER_URL = INTEGRATOR_URL + '/new_orders.php'
    DELETE_ORDER_URL = INTEGRATOR_URL + '/delete_orders.php'
    ORDER_STATUS_URL = INTEGRATOR_URL + '/status_report_h.php'
    ORDER_INFO_URL = INTEGRATOR_URL + '/info_report.php'
    ORDER_PRINT_URL = INTEGRATOR_URL + '/orders_print.php'
    DELIVERY_POINTS_URL = INTEGRATOR_URL + '/pvzlist.php'
    CALL_COURIER_URL = INTEGRATOR_URL + '/call_courier.php'


class TestCDEKClient(unittest.TestCase):
    """
    Тестирование класса Client для работы со СДЭК
    """
    __dms = []

    # Подготовка к тестам
    def setUp(self):

        # Тестовая учетная запись ИМ из документации СДЭК
        self.client_IM = TestClient('z9GRRu7FxmO53CQ9cFfI6qiy32wpfTkd',
                                    'w24JTCv4MnAcuRTx0oHjHLDtyt3I6IBq')
        # Тестовая учетная запись Доставки из документации СДЭК
        self.client_D = TestClient('7JM7K5twfzEV1ssCRklthcIPbbVZrZrZ',
                                   't8XBoL1rUofIK9dKoXVB3Tji2F2hPHSk')

        # Заказы, продублированные из example.py
        pickup_order = MyOrder()
        pickup_order.sender_city_id = 44
        pickup_order.sender_city_postcode = 111111
        pickup_order.shipping_price = 0
        pickup_order.recipient_name = 'Иванов Иван Иванович'
        pickup_order.recipient_phone = '+7 (999) 999-99-99'
        pickup_order.recipient_city_id = 270  # Новосибирск
        pickup_order.recipient_city_postcode = 630066  # Новосибирск
        pickup_order.shipping_tariff = 136  # самовывоз
        pickup_order.pvz_code = 'NSK71'
        pickup_order.is_paid = True
        pickup_order_line = MyOrderLine(order=pickup_order)
        pickup_order_line.quantity = 1
        pickup_order.lines = [pickup_order_line]
        self.pickup_order = pickup_order

        delivery_order = MyOrder()
        delivery_order.sender_city_id = 44
        delivery_order.sender_city_postcode = 111111
        delivery_order.shipping_price = 0
        delivery_order.pvz_code = ""
        delivery_order.recipient_name = 'Иванов Иван Иванович'
        delivery_order.recipient_phone = '+7 (999) 999-99-99'
        delivery_order.recipient_city_id = 137  # Санкт-Петербург
        delivery_order.recipient_city_postcode = 198261  # Санкт-Петербург
        delivery_order.recipient_address_street = 'пр. Ленина'
        delivery_order.recipient_address_house = 1
        delivery_order.recipient_address_flat = 1
        delivery_order.shipping_tariff = 139  # доставка дверь-дверь
        delivery_order.comment = 'Позвонить за час'
        delivery_order.is_paid = False

        order_line = MyOrderLine(order=delivery_order)
        order_line.quantity = 1
        delivery_order.lines = [order_line]
        self.delivery_order = delivery_order

        # Сохраняем пример простого вложенного xml
        parent = ElementTree.Element(
            'ParentElement',
            attrib={'isTestElement': "True", 'isParent': "True"}
        )
        ElementTree.SubElement(
            parent,
            'Good',
            attrib={'isTestElement': "True", 'isParent': "False"}
        )
        ElementTree.SubElement(
            parent,
            'SimpleChild',
            attrib={'isTestElement': "True", 'isParent': "False", 'number': "2"}
        )
        self.simple_xml = parent

        # Сохраняем простой xml в виде строки
        self.simple_xml_str = '<?xml version="1.0" encoding="UTF-8" ?>' \
                              '<ParentElement isParent="True" isTestElement="True">' \
                              '<Good isParent="False" isTestElement="True" />' \
                              '<SimpleChild isParent="False" isTestElement="True" number="2" />' \
                              '</ParentElement>'

        # Сохраняем простой xml в виде словаря
        self.simple_xml_dict = {
            'isTestElement': "True",
            'isParent': "True",
            'Good': [
                {
                    'isTestElement': "True",
                    'isParent': "False"
                }
            ],
            'SimpleChild': {
                'isTestElement': "True",
                'isParent': "False",
                'number': "2"
            }
        }

    # 1. Данные класса клиента для авторизации
    def test_get_user_info(self):
        client = TestClient(login='login', password='pswd')
        self.assertEqual(client._login, 'login')
        self.assertEqual(client._password, 'pswd')

    # 2. Конвертация xml в dict
    def test__xml_to_dict(self):
        # Используем созданный перед тестами пример xml
        xml = self.simple_xml
        # Ожидаемое возвращаемое значение
        expected_xml_dict = self.simple_xml_dict
        xml_dict = Client._xml_to_dict(xml)
        self.assertEqual(xml_dict, expected_xml_dict)

    # 3. Конвертация xml в строку
    def test__xml_to_string(self):
        test_client = TestClient('login', 'password')
        # Используем созданный перед тестами пример xml
        xml = self.simple_xml
        # Ожидаемое возвращаемое значение (в байтовой строке)
        expected_xml_string = self.simple_xml_str.encode("UTF-8")
        xml_string = test_client._xml_to_string(xml)
        self.assertEqual(xml_string, expected_xml_string)

    # 4. Генерация секретного ключа согласно документации
    def test__make_secure(self):
        date = '2016-09-25T12:45:10'
        # Из примера документации
        test_client = Client('test', '6bd3937dcebd15beb25278bc0657014c')
        secure_key = test_client._make_secure(date)
        self.assertEqual('81ad561784277fa864bf644d755fb164', secure_key)

    # 5. Выполнение запроса на создание заказа (доставка)
    def test__create_order_delivery(self):
        client = self.client_IM
        order = self.delivery_order
        order.number = 1
        response = client.create_order(order)
        # В ошибочном ответе DispatchNumber нет, поэтому его можно сохранять
        if 'DispatchNumber' in response:
            self.__dms.append(response['DispatchNumber'])
        # Если в ответе с сервера нет поля ErrorCode, то создание прошло успешно
        self.assertFalse('ErrorCode' in response)

    # 6. Выполнение запроса на создание заказа (самовывоз)
    def test__create_order_pickup(self):
        client = self.client_IM
        order = self.pickup_order
        order.number = 2
        response = client.create_order(order)
        # В ошибочном ответе DispatchNumber нет, поэтому его можно сохранять
        if 'DispatchNumber' in response:
            self.__dms.append(response['DispatchNumber'])
        # Если в ответе с сервера нет поля ErrorCode, то создание прошло успешно
        self.assertFalse('ErrorCode' in response)

    # 7. Выполнение запроса на получение информации о заказах
    def test__get_orders_info(self):
        client = self.client_IM
        dms = self.__dms
        response = client.get_orders_info(dms)
        # Если в ответе с сервера нет поля ErrorCode, то создание прошло успешно
        for resp in response:
            self.assertFalse('ErrorCode' in resp)

    # 8. Выполнение запроса на получение информации о заказах
    # с историей изменения статусов
    def test__get_orders_statuses_History(self):
        client = self.client_IM
        dms = self.__dms
        response = client.get_orders_statuses(dms, show_history=True)
        # Если в ответе с сервера нет поля ErrorCode, то создание прошло успешно
        for resp in response:
            self.assertFalse('ErrorCode' in resp)

    # 9. Выполнение запроса на получение информации о заказах
    # без истории изменения статусов
    def test__get_orders_statuses_No_History(self):
        client = self.client_IM
        dms = self.__dms
        response = client.get_orders_statuses(dms, show_history=False)
        # Если в ответе с сервера нет поля ErrorCode, то создание прошло успешно
        for resp in response:
            self.assertFalse('ErrorCode' in resp)

    # 10. Выполнение запроса на печать квитанций заказов
    def test__get_orders_print(self):
        client = self.client_IM
        dms = self.__dms
        response = client.get_orders_print(dms)
        # Если None, то произошла ошибка
        self.assertIsNotNone(response)

    # 11. Выполнение запроса на вызов курьера (без dispatch_number)
    def test_call_courier(self):
        client = self.client_IM
        order = self.delivery_order
        # Ожидание курьера
        call_params = {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'time_beg': datetime.time(13, 0, 0),
            'time_end': datetime.time(17, 15, 0),
            'send_city_code': order.get_sender_city_id(),
            'send_city_postcode': order.get_sender_postcode(),
            'send_phone': '+7 (999) 999-99-88',
            'sender_name': 'Отправитель Отправителевич Отправителев',
            'weight': 1000,
            'address': {
                'street': 'Уличная',
                'house': '1',
                'flat': '1'
            }
        }
        response = client.call_courier(call_params)
        # Если в ответе с сервера нет поля ErrorCode, то вызов курьера прошел успешно
        self.assertFalse('ErrorCode' in response)

    # 12. Выполнение запроса на вызов курьера (с dispatch_number)
    def test_call_courier_DN(self):
        client = self.client_IM
        order = self.delivery_order
        dn = ''
        if isinstance(self.__dms, list) and len(self.__dms) > 0:
            dn = self.__dms[0]
        # Ожидание курьера
        call_params = {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'time_beg': datetime.time(13, 0, 0),
            'time_end': datetime.time(17, 15, 0),
            # 'send_city_code': order.get_sender_city_id(), значение из накладной
            'send_city_postcode': order.get_sender_postcode(),
            'send_phone': '+7 (999) 999-99-88',  # т.к. нет в накладной
            'sender_name': 'Отправитель Отправителевич Отправителев',  # т.к. нет в накладной
            # 'weight': 1000, значение из накладной
            'address': {
                'street': 'Уличная',
                'house': '1',
                'flat': '1'
            }
        }
        response = client.call_courier(call_params, dispatch_number=dn)
        # Если в ответе с сервера нет поля ErrorCode, то вызов курьера прошел успешно
        self.assertFalse('ErrorCode' in response)

    # 13. Выполнение запроса на вызов курьера
    # ошибка: call_params = None
    def test_call_courier_error_CP_None(self):
        client = self.client_IM
        self.assertRaises(AttributeError, client.call_courier, None)

    # 14. Выполнение запроса на вызов курьера
    # ошибка: call_params != dict
    def test_call_courier_error_CP_Not_Dict(self):
        client = self.client_IM
        self.assertRaises(AttributeError, client.call_courier, ['a', 'b'])

    # 15. Выполнение запроса на вызов курьера
    # ошибка: отсутствует обязательный параметр
    def test_call_courier_error_CP_Not_Full(self):
        client = self.client_IM
        self.assertRaises(AttributeError, client.call_courier, {
            'send_phone': '+7 (999) 999-99-88',
            'sender_name': 'Отправитель Отправителевич Отправителев'
        })

    # 16. Выполнение запроса на вызов курьера
    # ошибка: отсутствует обязательный параметр у адреса
    def test_call_courier_error_CP_Address_Not_Full(self):
        client = self.client_IM
        order = self.delivery_order
        self.assertRaises(AttributeError, client.call_courier, {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'time_beg': datetime.time(13, 0, 0),
            'time_end': datetime.time(17, 15, 0),
            'send_city_code': order.get_sender_city_id(),
            'send_city_postcode': order.get_sender_postcode(),
            'send_phone': '+7 (999) 999-99-88',
            'sender_name': 'Отправитель Отправителевич Отправителев',
            'weight': 1000,
            'address': {
                'street': 'Уличная',
                'flat': '1'
            }
        })

    # 17. Выполнение запроса на вызов курьера
    # ошибка: HTTPError во время запроса
    def test_call_courier_HTTP_error(self):
        client = TestClient('login', 'password')
        order = self.delivery_order
        # Ожидание курьера
        call_params = {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'time_beg': datetime.time(13, 0, 0),
            'time_end': datetime.time(17, 15, 0),
            'send_city_code': order.get_sender_city_id(),
            'send_city_postcode': order.get_sender_postcode(),
            'send_phone': '+7 (999) 999-99-88',
            'sender_name': 'Отправитель Отправителевич Отправителев',
            'weight': 1000,
            'address': {
                'street': 'Уличная',
                'house': '1',
                'flat': '1'
            }
        }
        response = client.call_courier(call_params)
        # Если в ответе с сервера нет поля ErrorCode, то вызов курьера прошел успешно
        self.assertIsNone(response)

    # 18. Выполнение запроса на удаление заказа (доставка)
    def test_delete_order_delivery(self):
        client = self.client_IM
        order = self.delivery_order
        order.number = 1
        response = client.delete_order(order)
        # Если в ответе с сервера нет поля ErrorCode, то удаление прошло успешно
        self.assertFalse('ErrorCode' in response)

    # 19. Выполнение запроса на удаление заказа (самовывоз)
    # Данный тест добавлен для симметрии удаления созданного заказа
    # (что создано должно быть удалено, чтобы не вызвать проблем при новых тестах)
    def test_delete_order_pickup(self):
        client = self.client_IM
        order = self.pickup_order
        order.number = 2
        response = client.delete_order(order)
        # Если в ответе с сервера нет поля ErrorCode, то удаление прошло успешно
        self.assertFalse('ErrorCode' in response)
