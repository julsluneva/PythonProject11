import pytest

from src.processing import (filter_by_currency, filter_by_state, normalize_transaction_structure,
                            process_bank_operations, process_bank_search, sort_by_date)

bank_oper = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.fixture
def sample_data():
    return bank_oper.copy()


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("", []),
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    """Тестирование фильтрации операций по состоянию"""
    filtered = filter_by_state(sample_data, state)
    assert [x["id"] for x in filtered] == expected_ids


def test_filter_by_state_default(sample_data):
    """Тестирование фильтрации операций со значением по умолчанию"""
    filtered = filter_by_state(sample_data)
    assert [x["id"] for x in filtered] == [41428829, 939719570]


# Тесты для sort_by_date
# тестирования сортировки
@pytest.mark.parametrize("reverse, expected_first_date", [(True, 41428829), (False, 939719570)])
def test_sort_by_date(sample_data, reverse, expected_first_date):
    sorted_operations = sort_by_date(sample_data, reverse=reverse)
    assert sorted_operations[0]["id"] == expected_first_date


@pytest.mark.parametrize(
    "operations, reverse",
    [
        ([{"id": 1, "date": "2023-02-30T00:00:00"}], True),  # Некорректная дата (30 февраля)
        ([{"id": 2, "date": "not-a-date"}], False),  # Не дата, а строка
        ([], True),  # Пустой список
    ],
)
def test_sort_by_date_invalid(operations, reverse):
    """Тест обработки некорректных дат или пустого списка."""
    # Проверяем, что функция не падает и возвращает список (без проверки порядка)
    result = sort_by_date(operations, reverse=reverse)
    assert isinstance(result, list)


def test_filter_by_currency():
    """Тест фильтрации по валюте."""
    # JSON формат
    json_data = [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"name": "руб.", "code": "RUB"}}},
        {"id": 2, "operationAmount": {"amount": "50", "currency": {"name": "USD", "code": "USD"}}},
    ]
    # CSV формат
    csv_data = [
        {"id": 3, "amount": "200", "currency_name": "руб.", "currency_code": "RUB"},
        {"id": 4, "amount": "75", "currency_name": "EUR", "currency_code": "EUR"},
    ]

    # Тест 1: Фильтрация рублевых транзакций (JSON)
    result = filter_by_currency(json_data, rub_only=True)
    assert len(result) == 1
    assert result[0]["id"] == 1

    # Тест 2: Фильтрация рублевых транзакций (CSV)
    result = filter_by_currency(csv_data, rub_only=True)
    assert len(result) == 1
    assert result[0]["id"] == 3

    # Тест 3: Без фильтрации (все транзакции)
    result = filter_by_currency(json_data + csv_data, rub_only=False)
    assert len(result) == 4

    # Тест 4: Пустые данные
    result = filter_by_currency([], rub_only=True)
    assert len(result) == 0

    # Тест 5: Данные без информации о валюте
    data_no_currency = [{"id": 5, "description": "Операция"}]
    result = filter_by_currency(data_no_currency, rub_only=True)
    assert len(result) == 0


def test_normalize_transaction_structure():
    """Тест нормализации структуры транзакции."""
    # JSON транзакция
    json_tx = {"id": 1, "operationAmount": {"amount": "100.50", "currency": {"name": "руб.", "code": "RUB"}}}

    # CSV транзакция
    csv_tx = {"id": 2, "amount": "200.75", "currency_name": "USD", "currency_code": "USD"}

    # Тест 1: Нормализация JSON
    result = normalize_transaction_structure(json_tx)  # ИСПРАВЛЕНО
    assert result["amount"] == "100.50"
    assert result["currency_name"] == "руб."
    assert result["currency_code"] == "RUB"
    assert "operationAmount" in result  # Оригинальные данные сохраняются

    # Тест 2: Нормализация CSV
    result = normalize_transaction_structure(csv_tx)  # ИСПРАВЛЕНО
    assert result["amount"] == "200.75"
    assert result["currency_name"] == "USD"
    assert result["currency_code"] == "USD"

    # Тест 3: Транзакция без информации о сумме
    tx_no_amount = {"id": 3, "description": "Тест"}
    result = normalize_transaction_structure(tx_no_amount)  # ИСПРАВЛЕНО
    assert "amount" in result
    assert result["amount"] == ""
    assert result["currency_name"] == ""
    assert result["currency_code"] == ""

    # Тест 4: Транзакция с неправильной структурой
    tx_wrong_structure = {"id": 4, "operationAmount": "просто строка"}  # Не словарь
    result = normalize_transaction_structure(tx_wrong_structure)  # ИСПРАВЛЕНО
    assert isinstance(result, dict)


def test_process_bank_search():
    """Тест функции поиска транзакций по описанию."""
    test_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Перевод организации"},
        {"id": 5, "description": "None"},  # описание None
        {"id": 6},  # Нет описания
    ]

    # Тест 1: Поиск существующего слова
    result = process_bank_search(test_data, "организации")
    assert len(result) == 2
    assert all("организации" in t["description"].lower() for t in result)

    # Тест 2: Поиск несуществующего слова
    result = process_bank_search(test_data, "несуществующее")
    assert len(result) == 0

    # Тест 3: Поиск без учета регистра
    result = process_bank_search(test_data, "ПЕРЕВОД")
    assert len(result) == 3

    # Тест 4: Пустые данные
    result = process_bank_search([], "организации")
    assert len(result) == 0

    # Тест 5: Пустая строка поиска
    result = process_bank_search(test_data, "")
    assert len(result) == 0

    # Тест 6: Специальные символы в поиске
    result = process_bank_search(test_data, "Перевод")
    assert len(result) == 3

    # Тест 7: Частичное совпадение
    result = process_bank_search(test_data, "Перевод орга")
    assert len(result) == 2


def test_process_bank_operations():
    """Тест функции подсчета операций по категориям."""
    test_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Перевод организации"},
        {"id": 5, "description": "Перевод со счета на счет"},
        {"id": 6, "description": "None"},  # описание None
        {"id": 7},  # Нет описания
    ]

    categories = ["Перевод", "Открытие", "Пополнение", "вклад"]

    # Тест 1: Нормальный случай
    result = process_bank_operations(test_data, categories)
    assert result["Перевод"] == 4
    assert result["Открытие"] == 1
    assert result["Пополнение"] == 0
    assert result["вклад"] == 1  # Частичное совпадение

    # Тест 2: Без учета регистра
    categories_lower = ["перевод", "открытие"]
    result = process_bank_operations(test_data, categories_lower)
    assert result["перевод"] == 4
    assert result["открытие"] == 1

    # Тест 3: Пустые данные
    result = process_bank_operations([], categories)
    assert result == {"Перевод": 0, "Открытие": 0, "Пополнение": 0, "вклад": 0}

    # Тест 4: Пустой список категорий
    result = process_bank_operations(test_data, [])
    assert result == {}

    # Тест 5: Категории с пробелами
    categories_with_spaces = ["Перевод организации", "Открытие вклада"]
    result = process_bank_operations(test_data, categories_with_spaces)
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1


def test_process_bank_search_with_regex_special_chars():
    """Тест поиска со специальными символами RegEx."""
    test_data = [
        {"id": 1, "description": "Перевод 100$"},
        {"id": 2, "description": "Оплата 50%"},
        {"id": 3, "description": "test.*special[chars]"},
        {"id": 4, "description": "Перевод (срочный)"},
        {"id": 5, "description": "Оплата + комиссия"},
    ]

    # Тест с символами, которые имеют значение в RegEx
    result = process_bank_search(test_data, "100$")
    assert len(result) == 1
    assert result[0]["id"] == 1

    result = process_bank_search(test_data, "50%")
    assert len(result) == 1
    assert result[0]["id"] == 2

    result = process_bank_search(test_data, "test.*special[chars]")
    assert len(result) == 1
    assert result[0]["id"] == 3

    result = process_bank_search(test_data, "(срочный)")
    assert len(result) == 1
    assert result[0]["id"] == 4

    result = process_bank_search(test_data, "+ комиссия")
    assert len(result) == 1
    assert result[0]["id"] == 5


def test_filter_by_state_case_insensitive():
    """Тест фильтрации по статусу без учета регистра."""
    test_data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "executed"},
        {"id": 3, "state": "ExEcUtEd"},
        {"id": 4, "state": "CANCELED"},
    ]

    result = filter_by_state(test_data, "EXECUTED")
    assert len(result) == 3
    assert all(t["id"] in [1, 2, 3] for t in result)

    result = filter_by_state(test_data, "executed")
    assert len(result) == 3


def test_sort_by_date_empty_and_single():
    """Тест сортировки пустого списка и списка с одним элементом."""
    # Пустой список
    result = sort_by_date([])
    assert result == []

    # Один элемент
    single = [{"id": 1, "date": "2023-01-01T00:00:00Z"}]
    result = sort_by_date(single)
    assert result == single

    result = sort_by_date(single, reverse=False)
    assert result == single


def test_filter_by_currency_various_formats():
    """Тест фильтрации валют в различных форматах."""
    test_data = [
        {"id": 1, "currency_name": "руб."},
        {"id": 2, "currency_name": "RUB"},
        {"id": 3, "currency_name": "Ruble"},
        {"id": 4, "currency_name": "USD"},
        {"id": 5, "currency_name": "RUB"},
        {"id": 6, "currency_name": "USD"},
        {"id": 7, "operationAmount": {"currency": {"name": "руб."}}},
        {"id": 8, "operationAmount": {"currency": {"code": "RUB"}}},
    ]

    result = filter_by_currency(test_data, rub_only=True)
    # ID 1, 2, 3, 5, 7, 8 - рублевые
    assert len(result) == 6
    assert all(t["id"] in [1, 2, 3, 5, 7, 8] for t in result)


def test_process_bank_operations_case_insensitive():
    """Тест подсчета категорий без учета регистра."""
    test_data = [
        {"id": 1, "description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},
        {"id": 2, "description": "открытие вклада"},
        {"id": 3, "description": "Перевод с карты на карту"},
    ]

    categories = ["Перевод", "Открытие", "Вклад"]
    result = process_bank_operations(test_data, categories)

    assert result["Перевод"] == 2  # id 1,3
    assert result["Открытие"] == 1  # id 2
    assert result["Вклад"] == 1  # id 2 (частичное совпадение)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
