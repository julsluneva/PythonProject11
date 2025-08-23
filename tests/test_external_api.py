import os
from unittest.mock import Mock, patch

import pytest

from src.external_api import cached_rates, convert_currency, get_exchange_rate


def test_get_exchange_rate_cached():
    """Тестирование получения курса из кэша"""
    # Очищаем кэш перед тестом
    cached_rates.clear()
    # Добавляем тестовые данные в кэш
    test_cache_key = "USD_RUB"
    test_rate = 75.5
    cached_rates[test_cache_key] = test_rate
    # Вызываем функцию, она должна вернуть данные из кэша
    result = get_exchange_rate("USD", "RUB")
    assert result == test_rate
    assert len(cached_rates) == 1  # Кэш не должен измениться


@patch("os.getenv")
def test_get_exchange_rate_api_key_missing(mock_getenv):
    """Тестирование ошибки при отсутствии API ключа"""
    mock_getenv.return_value = None
    with pytest.raises(ValueError, match="API key not found"):
        get_exchange_rate("USD", "RUB")


@patch("requests.get")
def test_get_exchange_rate_success(mock_get):
    """Тестирование успешного получения курса через API"""
    # Очищаем кэш перед тестом
    cached_rates.clear()
    # Мокируем ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 80.1234}, "base": "USD"}
    mock_get.return_value = mock_response
    # Мокируем переменную окружения
    with patch.dict(os.environ, {"API_KEY": "test_key"}):
        result = get_exchange_rate("USD", "RUB")
    # Проверяем результат и кэш
    assert result == 80.1234
    assert cached_rates["USD_RUB"] == 80.1234
    mock_get.assert_called_once()


@patch("requests.get")
def test_get_exchange_rate_api_error(mock_get):
    """Тестирование ошибки API"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    with patch.dict(os.environ, {"API_KEY": "test_key"}):
        with pytest.raises(Exception, match="API error: Status code 401"):
            get_exchange_rate("USD", "RUB")


@patch("requests.get")
def test_get_exchange_rate_network_error(mock_get):
    """Тестирование сетевой ошибки"""
    mock_get.side_effect = ConnectionError("Network problem")
    with patch.dict(os.environ, {"API_KEY": "test_key"}):
        with pytest.raises(Exception, match="Network problem"):
            get_exchange_rate("USD", "RUB")


def test_convert_currency_rub():
    """Тестирование конвертации из RUB в 'RUB"""
    transaction_data = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}
    result = convert_currency(transaction_data)
    assert result == 1000.50


@patch("src.external_api.get_exchange_rate")
def test_convert_currency_usd(mock_get_rate):
    """Тестирование конвертации USD в RUB"""
    mock_get_rate.return_value = 75.5
    transaction_data = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    result = convert_currency(transaction_data)
    assert result == 7550.0
    mock_get_rate.assert_called_once_with("USD")


@patch("src.external_api.get_exchange_rate")
def test_convert_currency_eur(mock_get_rate):
    """Тестирование конвертации EUR в RUB"""
    mock_get_rate.return_value = 82.5

    transaction_data = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}
    result = convert_currency(transaction_data)
    assert result == 4125.0  # 50 * 82.5
    mock_get_rate.assert_called_once_with("EUR")


def test_convert_currency_other_currency():
    """Тестирование конвертации неизвестной валюты"""
    transaction_data = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}  # Фунт стерлингов
    result = convert_currency(transaction_data)
    assert result == 100.00  # Исходная сумма


def test_convert_currency_invalid_amount_format():
    """Тестирование ошибки неверного формата суммы"""
    transaction_data = {"operationAmount": {"amount": "not_a_number", "currency": {"code": "USD"}}}
    with pytest.raises(ValueError, match="Invalid amount format"):
        convert_currency(transaction_data)


def test_convert_currency_missing_key():
    """Тестирование ошибки отсутствия обязательного ключа"""
    transaction_data = {
        "operationAmount": {
            "amount": "100.00"
            # Отсутствует currency
        }
    }
    with pytest.raises(ValueError, match="Invalid transaction data format"):
        convert_currency(transaction_data)


def test_convert_currency_empty_data():
    """Тестирование ошибки пустых данных"""
    with pytest.raises(ValueError, match="Invalid transaction data format"):
        convert_currency({})


@patch("src.external_api.get_exchange_rate")
def test_convert_currency_api_error_propogation(mock_get_rate):
    """Тестирование распространения ошибки из get_exchange_rate"""
    mock_get_rate.side_effect = Exception("API unavailable")
    transaction_data = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    with pytest.raises(Exception, match="Currency conversion failed"):
        convert_currency(transaction_data)
