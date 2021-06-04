from decimal import Decimal
from pycbrf.toolbox import ExchangeRates
from datetime import datetime


def convert_rub(summa=0) -> Decimal:
    today = datetime.today().strftime("%Y-%m-%d")
    rates = ExchangeRates(today)

    usd = rates['USD'].value
    eur = rates['EUR'].value

    return round(usd, 2), round(eur, 2), [round(summa/usd, 2), round(summa/eur, 2)]


def check_int(n):
    try:
        i = int(n)
        return True
    except:
        return False