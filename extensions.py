import requests
import json

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)
        data = json.loads(response.text)
        if 'error' in data:
            raise APIException(data['error'])
        conversion_rate = data['rates'].get(quote)
        if not conversion_rate:
            raise APIException(f"Invalid currency: {quote}")
        result = conversion_rate * amount
        return result

class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)