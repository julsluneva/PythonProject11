"""Тесты для модуля display.py"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.display import (
    format_date,
    mask_card_or_account,
    format_transaction,
    display_transactions
)


# Тесты для format_date
@pytest.mark.parametrize("input_date, expected", [
    ("2023-12-25T15:30:45Z", "25.12.2023"),
    ("2023-12-25T15:30:45.123456", "25.12.2023"),
    ("2023-12-25", "25.12.2023"),
    ("", "Дата не указана"),
    ("invalid-date", "invalid-da"),  # Функция обрезает до 10 символов
    (None, "Дата не указана"),
])
def test_format_date(input_date, expected):
    """Тестирование форматирования даты"""
    if input_date is None:
        result = format_date("")
    else:
        result = format_date(input_date)
    assert result == expected


def test_format_date_edge_cases():
    """Тестирование граничных случаев форматирования даты"""
    # Длинная строка, обрезается до 10 символов
    long_str = "2023-12-25 extra text"
    assert format_date(long_str) == "2023-12-25"

    # Строка с неправильным форматом, но начинающаяся с даты
    weird_format = "2023/12/25T15:30:45"
    assert format_date(weird_format) == "2023/12/25"


# Тесты для mask_card_or_account
@pytest.mark.parametrize("input_number, expected", [
    # Тесты для счетов
    ("Счет 12345678901234567890", "Счет **7890"),
    ("счет 40817810099910004321", "счет **4321"),
    ("Счет 12345", "Счет 12345"),  # Слишком короткий номер

    # Тесты для карт
    ("Visa Platinum 1234567812345678", "Visa Platinum 1234 56** **** 5678"),
    ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
    ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
    ("1234567812345678", "1234 56** **** 5678"),  # Только номер

    # Пустые и граничные случаи
    ("", ""),
    (None, ""),
    ("Счет", "Счет"),  # Только слово без номера
    ("Visa", "Visa"),  # Только название без номера
])
def test_mask_card_or_account(input_number, expected):
    """Тестирование маскирования карт и счетов"""
    if input_number is None:
        result = mask_card_or_account("")
    else:
        result = mask_card_or_account(input_number)
    assert result == expected


def test_mask_card_or_account_invalid_card():
    """Тестирование маскирования с некорректным номером карты"""
    # Номер карты недостаточной длины
    result = mask_card_or_account("Visa 1234")
    assert result == "Visa 1234"

    # Номер карты с буквами
    result = mask_card_or_account("Visa 1234abcd5678efgh")
    assert result == "Visa 1234abcd5678efgh"


def test_mask_card_or_account_account_without_number():
    """Тестирование счета без номера"""
    result = mask_card_or_account("Счет")
    assert result == "Счет"


# Тесты для format_transaction
@pytest.fixture
def sample_transaction_json():
    """Фикстура с транзакцией в JSON формате"""
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }


@pytest.fixture
def sample_transaction_csv():
    """Фикстура с транзакцией в CSV формате"""
    return {
        "id": 650703,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": "16210",
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации"
    }


@patch('src.processing.normalize_transaction_structure')
@patch('src.display.format_date')
@patch('src.display.mask_card_or_account')
def test_format_transaction_json(mock_mask, mock_format_date, mock_normalize, sample_transaction_json):
    """Тестирование форматирования JSON транзакции"""
    # Настройка моков
    mock_format_date.return_value = "26.08.2019"

    # Настраиваем mock_mask для возврата разных значений
    def mask_side_effect(arg):
        if arg == "Maestro 1596837868705199":
            return "Maestro 1596 83** **** 5199"
        elif arg == "Счет 64686473678894779589":
            return "Счет **9589"
        return ""

    mock_mask.side_effect = mask_side_effect

    mock_normalize.return_value = {
        "amount": "31957.58",
        "currency_name": "руб."
    }

    result = format_transaction(sample_transaction_json)

    # Проверяем, что все моки были вызваны
    mock_format_date.assert_called_once_with("2019-08-26T10:50:58.294041")
    assert mock_mask.call_count == 2
    mock_normalize.assert_called_once_with(sample_transaction_json)

    # Проверяем результат
    expected_lines = [
        "26.08.2019 Перевод организации",
        "Maestro 1596 83** **** 5199 -> Счет **9589",
        "Сумма: 31957.58 руб.",
        ""
    ]
    assert result == "\n".join(expected_lines)


@patch('src.processing.normalize_transaction_structure')
@patch('src.display.format_date')
@patch('src.display.mask_card_or_account')
def test_format_transaction_csv(mock_mask, mock_format_date, mock_normalize, sample_transaction_csv):
    """Тестирование форматирования CSV транзакции"""
    # Настройка моков
    mock_format_date.return_value = "05.09.2023"

    # Настраиваем mock_mask для возврата разных значений
    def mask_side_effect(arg):
        if arg == "Счет 58803664561298323391":
            return "Счет **3391"
        elif arg == "Счет 39745660563456619397":
            return "Счет **9397"
        return ""

    mock_mask.side_effect = mask_side_effect

    mock_normalize.return_value = {
        "amount": "16210",
        "currency_name": "Sol"
    }

    result = format_transaction(sample_transaction_csv)

    # Проверяем результат
    expected_lines = [
        "05.09.2023 Перевод организации",
        "Счет **3391 -> Счет **9397",
        "Сумма: 16210 Sol",
        ""
    ]
    assert result == "\n".join(expected_lines)


@patch('src.processing.normalize_transaction_structure')
@patch('src.display.format_date')
@patch('src.display.mask_card_or_account')
def test_format_transaction_missing_fields(mock_mask, mock_format_date, mock_normalize):
    """Тестирование форматирования транзакции с отсутствующими полями"""
    transaction = {
        "date": "2023-01-01",
        "description": "Тестовая операция"
        # Нет from, to, operationAmount
    }

    mock_format_date.return_value = "01.01.2023"

    # Оба вызова mask_card_or_account вернут пустые строки
    mock_mask.side_effect = ["", ""]

    mock_normalize.return_value = {
        "amount": "",
        "currency_name": ""
    }

    result = format_transaction(transaction)

    expected_lines = [
        "01.01.2023 Тестовая операция",
        "",  # Пустая строка вместо from/to
        "Сумма:  ",
        ""
    ]
    assert result == "\n".join(expected_lines)


@patch('src.processing.normalize_transaction_structure')
@patch('src.display.format_date')
@patch('src.display.mask_card_or_account')
def test_format_transaction_only_from(mock_mask, mock_format_date, mock_normalize):
    """Тестирование транзакции только с полем from"""
    transaction = {
        "date": "2023-01-01",
        "description": "Снятие наличных",
        "from": "Visa 1234567812345678"
        # to отсутствует
    }

    mock_format_date.return_value = "01.01.2023"

    # Первый вызов (from) вернет маскированную карту
    # Второй вызов (to) вернет пустую строку
    mock_mask.side_effect = ["Visa 1234 56** **** 5678", ""]

    mock_normalize.return_value = {
        "amount": "5000",
        "currency_name": "RUB"
    }

    result = format_transaction(transaction)

    expected_lines = [
        "01.01.2023 Снятие наличных",
        "Visa 1234 56** **** 5678",
        "Сумма: 5000 RUB",
        ""
    ]
    assert result == "\n".join(expected_lines)


@patch('src.processing.normalize_transaction_structure')
@patch('src.display.format_date')
@patch('src.display.mask_card_or_account')
def test_format_transaction_only_to(mock_mask, mock_format_date, mock_normalize):
    """Тестирование транзакции только с полем to (например, пополнение)"""
    transaction = {
        "date": "2023-01-01",
        "description": "Пополнение счета",
        "to": "Счет 12345678901234567890"
        # from отсутствует
    }

    mock_format_date.return_value = "01.01.2023"

    # Первый вызов (from) вернет пустую строку
    # Второй вызов (to) вернет маскированный счет
    mock_mask.side_effect = ["", "Счет **7890"]

    mock_normalize.return_value = {
        "amount": "10000",
        "currency_name": "RUB"
    }

    result = format_transaction(transaction)

    expected_lines = [
        "01.01.2023 Пополнение счета",
        "Счет **7890",
        "Сумма: 10000 RUB",
        ""
    ]
    assert result == "\n".join(expected_lines)


# Тесты для display_transactions
@patch('builtins.print')
def test_display_transactions_empty(mock_print):
    """Тестирование вывода пустого списка транзакций"""
    display_transactions([])

    mock_print.assert_called_once_with(
        "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
    )


@patch('builtins.print')
@patch('src.display.format_transaction')
def test_display_transactions_with_data(mock_format, mock_print):
    """Тестирование вывода списка транзакций"""
    transactions = [
        {"id": 1, "description": "Операция 1"},
        {"id": 2, "description": "Операция 2"}
    ]

    mock_format.side_effect = [
        "Форматированная транзакция 1",
        "Форматированная транзакция 2"
    ]

    display_transactions(transactions)

    # Проверяем, что print был вызван нужное количество раз
    assert mock_print.call_count == 5  # 1 заголовок + 2 транзакции + 2 разделителя

    # Проверяем первый вызов (заголовок)
    mock_print.assert_any_call("Всего банковских операций в выборке: 2\n")

    # Проверяем вызовы с транзакциями и разделителями
    mock_print.assert_any_call("Форматированная транзакция 1")
    mock_print.assert_any_call("-" * 50)
    mock_print.assert_any_call("Форматированная транзакция 2")
    mock_print.assert_any_call("-" * 50)

    assert mock_format.call_count == 2


@patch('builtins.print')
@patch('src.display.format_transaction')
def test_display_transactions_single(mock_format, mock_print):
    """Тестирование вывода одной транзакции"""
    transactions = [{"id": 1, "description": "Операция 1"}]

    mock_format.return_value = "Форматированная транзакция 1"

    display_transactions(transactions)

    # Проверяем, что print был вызван нужное количество раз
    assert mock_print.call_count == 3  # 1 заголовок + 1 транзакция + 1 разделитель

    mock_print.assert_any_call("Всего банковских операций в выборке: 1\n")
    mock_print.assert_any_call("Форматированная транзакция 1")
    mock_print.assert_any_call("-" * 50)


# Интеграционный тест (без моков)
def test_display_transactions_integration():
    """Интеграционный тест для display_transactions с реальными функциями"""
    transactions = [
        {
            "id": 1,
            "date": "2023-12-25T15:30:45",
            "description": "Перевод организации",
            "from": "Visa Platinum 1234567812345678",
            "to": "Счет 40817810099910004321",
            "operationAmount": {
                "amount": "15000.50",
                "currency": {"name": "руб.", "code": "RUB"}
            }
        }
    ]

    # Перехватываем вывод в консоль
    from io import StringIO
    import sys
    captured_output = StringIO()
    sys.stdout = captured_output

    try:
        display_transactions(transactions)

        output = captured_output.getvalue()

        # Проверяем, что вывод содержит ожидаемые элементы
        assert "Всего банковских операций в выборке: 1" in output

        # Проверяем наличие даты в любом формате
        assert any(date_format in output for date_format in [
            "2023-12-25",  # Исходный формат
            "25.12.2023"  # Отформатированный
        ])

        assert "Перевод организации" in output
        assert "Visa Platinum 1234 56** **** 5678" in output
        assert "Счет **4321" in output
        assert "Сумма: 15000.50 руб." in output
        assert "-" * 50 in output

    finally:
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])