import requests
import json
from config import EXCHANGE_TOKEN, API_URL

Currencies = {
    "RUR": "Russian ruble",
    "USD": "US dollar",
    "CAD": "Canadian dollar",
    "GBP": "British pound",
    "EUR": "European Euro",
}


class CurrencyConverter:
    @staticmethod
    def convert_currency(target, quote, amount):
        api_ = f'{API_URL}{EXCHANGE_TOKEN}/pair/{target}/{quote}/{amount}'
        r = requests.get(api_)
        d = json.loads(r.content)
        return (d.get("conversion_result"))


class InputException(Exception):
    pass
class APIException(Exception):
    pass
