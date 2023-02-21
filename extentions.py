import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f"Нельзя конвертировать одинаковые валюты: {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f"Не получилось конвертировать валюту: {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f"Не получилось конвертировать валюту: {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f"Не удалось конвертировать количество валюты: {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base
