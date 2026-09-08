from zoneinfo import ZoneInfo
import environ

env = environ.Env()

def format_currency(amount, symbol="Ar", decimal_places=2):
    formatted_amount = f"{amount:,.{decimal_places}f}"
    # formatted_amount = formatted_amount.replace(',', ' ')
    formatted_amount = f"{formatted_amount} {symbol}"
    return formatted_amount


def format_date(date, user_tz_name: str = "Africa/Nairobi"):
    user_tz = ZoneInfo(user_tz_name)
    utc_date = date
    local_date = utc_date.astimezone(user_tz)
    return local_date.strftime("%d-%m-%Y %H:%M:%S")