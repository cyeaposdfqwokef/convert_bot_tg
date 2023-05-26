import requests

class CurrencyConverter:
    @staticmethod
    def get_price(base_currency, quote_currency, amount):
        url = 'https://www.cbr.ru/currency_base/daily/'
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text

            base_currency_code_start = html_content.find(base_currency.upper())
            if base_currency_code_start == -1:
                raise APIException(f"Не удалось найти информацию для валюты {base_currency}")
            base_currency_rate_start = html_content.find('<td>', base_currency_code_start) + 4
            base_currency_rate_end = html_content.find('</td>', base_currency_rate_start)
            base_currency_rate = float(html_content[base_currency_rate_start:base_currency_rate_end].replace(',', '.'))

            quote_currency_code_start = html_content.find(quote_currency.upper())
            if quote_currency_code_start == -1:
                raise APIException(f"Не удалось найти информацию для валюты {quote_currency}")
            quote_currency_rate_start = html_content.find('<td>', quote_currency_code_start) + 4
            quote_currency_rate_end = html_content.find('</td>', quote_currency_rate_start)
            quote_currency_rate = float(html_content[quote_currency_rate_start:quote_currency_rate_end].replace(',', '.'))

            try:
                amount = float(amount)
            except ValueError:
                raise APIException("Неправильно введено число")

            converted_amount = (amount * quote_currency_rate) / base_currency_rate
            return converted_amount

        else:
            raise APIException("Не удалось получить курс валют")

class APIException(Exception):
    pass