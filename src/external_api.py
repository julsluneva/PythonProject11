import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()
cached_rates: dict[str, float] = {}


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> float:
    """Получает текущий курс валюты к рублю(по умолчанию)"""
    # Проверяем, есть ли курс в кэше
    cache_key = f"{from_currency}_{to_currency}"
    if cache_key in cached_rates:
        return cached_rates[cache_key]

    # Получаем API ключ из переменной окружения
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": api_key}
    params = {"base": from_currency, "symbols": to_currency}

    # Делаем запрос с ограничением по времени 10 сек
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        # Проверка статуса
        if response.status_code != 200:
            raise Exception(f"API error: Status code {response.status_code}")

        data = response.json()

        # Сохраняем курс в кэш
        exchange_rate = data["rates"][to_currency]
        cached_rates[cache_key] = exchange_rate
        return exchange_rate

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")
    except KeyError as e:
        raise Exception(f"Invalid response format: {e}")


def convert_currency(transaction_data: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли(float)"""
    try:
        # Извлекаем данные из транзакции
        amount_str = transaction_data["operationAmount"]["amount"]
        currency_code = transaction_data["operationAmount"]["currency"]["code"]
        amount = float(amount_str)

        # Если валюта уже в рублях, то возвращаем, как есть
        if currency_code == "RUB":
            return amount
        # Конвертируем USD и EUR в рубли
        if currency_code in ["USD", "EUR"]:
            exchange_rate = get_exchange_rate(currency_code)
            return amount * exchange_rate
        return amount

    except KeyError as e:
        raise ValueError(f"Invalid transaction data format: missing key {e}")
    except ValueError as e:
        raise ValueError(f"Invalid amount format: {e}")
    except Exception as e:
        raise Exception(f"Currency conversion failed: {e}")
