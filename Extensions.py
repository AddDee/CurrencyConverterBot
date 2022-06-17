import requests
import json
from Configuration import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base:str, sym:str, amount:str):

        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Вы конвертируете одну и туже валюту {base}!')

        try:
            amount = float(amount.replace(",","."))
        except ValueError:
            raise APIException(f'Не удалось конвертировать {amount}!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)[base_key]
        total_sum = resp[sym_key]* float(amount)
        text = f"{amount} {base} в {sym} - {total_sum}"
        return total_sum
