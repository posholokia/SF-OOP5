from config import *
import json
import requests


# собственный класс исключений - ошибки пользователя
class APIException(Exception):
    pass


# проверяем, что команда введена без ошибок и возвращаем котировку валют
class ExchangeCurrency:
    @staticmethod
    def get_price(quote, base, amount):
        try:  # проверяем, что валюта есть в словаре
            keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')
        try:
            keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')
        try:  # проверяем, что количество валюты - это целое число
            int(amount)
        except ValueError:
            raise APIException(f'Неверное значение количества валюты: {amount}')
        # отправляем API запрос и получаем котировку валюты
        rate = requests.get(f'https://currate.ru/api/?get=rates&pairs={keys[quote]}{keys[base]}&key={API_KEY}').content
        rate = float(json.loads(rate)['data'][f'{keys[quote]}{keys[base]}'])
        return rate

