from typing import Any

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстуры для тестов
@pytest.fixture
def valid_card_number() -> int:
    return 1234567812345678


@pytest.fixture
def valid_account_number() -> int:
    return 1234567890


#  тестирование функции маскировки номера карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567812345678, "1234 56** **** 5678"),
        (1111222233334444, "1111 22** **** 4444"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_get_mask_card_number_valid(card_number: int, expected: str):
    """Тестирование функции маскировки номера карты с валидными данными"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card_number, expected_exception",
    [
        (123456781234567, ValueError),  # Недостаточно цифр
        (12345678123456789, ValueError),  # Слишком много цифр
        ("1234abcd5678efgh", ValueError),  # Не цифровые символы
        ("", ValueError),  # Пустая строка
    ],
)
def test_get_mask_card_number_invalid(invalid_card_number: Any, expected_exception: Any):
    """Тестирование функции маскировки номера карты с невалидными данными"""
    with pytest.raises(expected_exception):
        get_mask_card_number(invalid_card_number)


# Параметризация для тестирования функции маскировки номера счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        (1234567890, "**7890"),
        (9876543210, "**3210"),
        (1000000001, "**0001"),
        (123456, "**3456"),  # Минимально допустимая длина
    ],
)
def test_get_mask_account_valid(account_number: int, expected: str):
    """Тестирование функции маскировки номера счета с валидными данными"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account_number, expected_exception",
    [
        (12345, ValueError),  # Недостаточно цифр
        ("abcdefghij", ValueError),  # Не цифровые символы
        ("", ValueError),  # Пустая строка
    ],
)
def test_get_mask_account_invalid(invalid_account_number: Any, expected_exception: Any):
    """Тестирование функции маскировки номера счета с невалидными данными"""
    with pytest.raises(expected_exception):
        get_mask_account(invalid_account_number)


# Тесты с использованием фикстур
def test_get_mask_card_number_with_fixture(valid_card_number: int):
    """Тестирование с использованием фикстуры для номера карты"""
    assert get_mask_card_number(valid_card_number) == "1234 56** **** 5678"


def test_get_mask_account_with_fixture(valid_account_number: int):
    """Тестирование с использованием фикстуры для номера счета"""
    assert get_mask_account(valid_account_number) == "**7890"
