# import pytest
#
#
# @pytest.fixture(autouse=True)
# def clear_cache():
#     """Фикстура для очистки кэша перед каждым тестом"""
#     from src.external_api import cached_rates
#
#     cached_rates.clear()
#     yield
#     cached_rates.clear()

"""Конфигурация для тестов pytest"""

import os
import sys
import warnings
from unittest.mock import patch

import pytest

# Подавляем предупреждение о sys.modules
warnings.filterwarnings("ignore", message=".*found in sys.modules after import.*", category=RuntimeWarning)


# Добавляем корень проекта в sys.path для импортов
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(autouse=True)
def clear_cache():
    """Фикстура для очистки кэша перед каждым тестом"""
    from src.external_api import cached_rates

    cached_rates.clear()
    yield
    cached_rates.clear()


@pytest.fixture
def mock_input():
    """Фикстура для мока input"""
    with patch("main.input") as mock:
        yield mock


@pytest.fixture
def mock_print():
    """Фикстура для мока print"""
    with patch("main.print") as mock:
        yield mock


@pytest.fixture
def mock_transactions():
    """Фикстура с тестовыми транзакциями для main тестов"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "description": "Перевод организации",
            "from": "Счет 12345678901234567890",
            "to": "Счет 98765432109876543210",
            "operationAmount": {"amount": "100.50", "currency": {"name": "руб.", "code": "RUB"}},
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T11:00:00",
            "description": "Открытие вклада",
            "to": "Счет 55555555555555555555",
            "operationAmount": {"amount": "200.75", "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2023-01-03T12:00:00",
            "description": "Перевод с карты на карту",
            "from": "Visa 1234567890123456",
            "to": "Mastercard 9876543210987654",
            "operationAmount": {"amount": "300.25", "currency": {"name": "EUR", "code": "EUR"}},
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2023-01-04T13:00:00",
            "description": "Перевод организации",
            "from": "Счет 11111111111111111111",
            "to": "Счет 22222222222222222222",
            "operationAmount": {"amount": "400.00", "currency": {"name": "руб.", "code": "RUB"}},
        },
    ]


@pytest.fixture
def mock_csv_transactions():
    """Фикстура с тестовыми транзакциями в CSV формате"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "amount": "100.50",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Счет 12345678901234567890",
            "to": "Счет 98765432109876543210",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T11:00:00",
            "amount": "200.75",
            "currency_name": "USD",
            "currency_code": "USD",
            "to": "Счет 55555555555555555555",
            "description": "Открытие вклада",
        },
    ]
