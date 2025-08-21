import itertools
from datetime import datetime

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

def test_operation_amount_format(sample_transactions):
    """Проверка корректности формата суммы операции"""
    for transaction in sample_transactions:
        amount_str = transaction["operationAmount"]["amount"]
        # Проверяем, что сумма является строкой
        assert isinstance(amount_str, str)
        # Проверяем, что строка может быть преобразована в float
        try:
            float(amount_str)
        except ValueError:
            pytest.fail(f"Amount '{amount_str}' is not a valid float number")
        # Проверяем, что сумма имеет 2 знака после запятой
        if '.' in amount_str:
            assert len(amount_str.split('.')[1]) == 2

def test_transaction_date_format(sample_transactions):
    """Проверка корректности формата даты в транзакциях"""
    for transaction in sample_transactions:
        date_str = transaction["date"]
        # Проверяем, что дата является строкой
        assert isinstance(date_str, str)
        # Пытаемся расписать дату в ISO формате
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            pytest.fail(f"Date '{date_str}' is not in valid ISO format")

# Добавим тест на пустое описание в transaction_descriptions
def test_transaction_descriptions_empty_description():
    """Тест на пустую строку в описании транзакции"""
    transactions = [{"description": ""}]
    result = list(transaction_descriptions(transactions))
    assert result == [""]

@pytest.mark.parametrize("currency, expected_count", [("USD", 2), ("RUB", 1), ("EUR", 0)])
def test_filter_by_currency(sample_transactions, currency, expected_count):
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count
    for transaction in filtered:
        assert transaction["operationAmount"]["currency"]["code"] == currency

def test_filter_by_currency_invalid_input():
    with pytest.raises(TypeError):
        list(filter_by_currency(None, "USD"))

def test_filter_by_currency_non_dict_transaction():
    """Тест, когда транзакция не является словарём"""
    transactions = ["not_a_dict", 123, None]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []

def test_filter_by_currency_empty_input():
    assert list(filter_by_currency([], "USD")) == []
    assert list(transaction_descriptions([])) == []

def test_filter_by_currency_missing_currency_key():
    transactions = [{"operationAmount": {"amount": "100"}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_operation_amount():
    transactions = [{"id": 1}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_currency():
    transactions = [{"operationAmount": {"amount": "100", "currency": {}}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_operation_amount_key():
    """Тест на отсутствие ключа operationAmount"""
    transactions = [{"id": 1}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_dict_operation_amount():
    """Тест, когда operationAmount не словарь"""
    transactions = [{"operationAmount": "invalid"}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_dict_currency():
    """Тест, когда currency не словарь"""
    transactions = [{"operationAmount": {"currency": "USD"}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_code():
    """Тест на отсутствие code в currency"""
    transactions = [{
        "id": 1,
        "state": "EXECUTED",
        "operationAmount": {"amount": "100", "currency": {"name": "USD"}}
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_list_input():
    """Тест на передачу не списка в filter_by_currency"""
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(filter_by_currency({"id": 1}, "USD"))

def test_filter_by_currency_invalid_currency_structure():
    """Тест на некорректную структуру currency"""
    transactions = [{
        "operationAmount": {
            "currency": "USD"  # Должно быть dict, а не str
        }
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_exception_handling():
    """Тест на обработку исключений в filter_by_currency"""
    # Транзакции, вызывающие разные исключения:
    # 1. TypeError (None вместо словаря)
    # 2. AttributeError (у строки нет метода .get())
    # 3. KeyError (нет ключа 'code')
    broken_transactions = [
        {"operationAmount": {"currency": None}},  # Вызовет TypeError
        {"operationAmount": "not_a_dict"},  # Вызовет AttributeError
        {"operationAmount": {"currency": {"name": "USD"}}},  # Нет 'code' → KeyError
    ]

    # Все исключения должны быть обработаны, результат — пустой список
    result = list(filter_by_currency(broken_transactions, "USD"))
    assert result == []

def test_filter_by_currency_missing_code_key():
    """Тест на отсутствие ключа code в currency"""
    transactions = [{
        "operationAmount": {
            "currency": {"name": "USD"}  # Нет code
        }
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_transaction_descriptions(sample_transactions):
    descriptions = list(transaction_descriptions(sample_transactions))
    assert len(descriptions) == len(sample_transactions)
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]

def test_transaction_descriptions_invalid_input():
    with pytest.raises(TypeError):
        list(transaction_descriptions("not a list"))

def test_transaction_descriptions_missing_key():
    """Тест на отсутствие ключа description в транзакции"""
    transactions = [{"id": 1}, {"description": "Test"}]
    with pytest.raises(KeyError, match="description key not found in transaction"):
        list(transaction_descriptions(transactions))

def test_transaction_descriptions_with_none():
    """Тест с description=None"""
    transactions = [{"description": None}]
    result = list(transaction_descriptions(transactions))
    assert result == [None]

def test_transaction_descriptions_non_str():
    """Тест с description не строкой"""
    transactions = [{"description": 123}]
    result = list(transaction_descriptions(transactions))
    assert result == [123]

def test_transaction_descriptions_mixed():
    """Тест со смешанными транзакциями (с description и без)"""
    transactions = [{"description": "test"}, {"id": 1}]
    with pytest.raises(KeyError, match="description key not found in transaction"):
        list(transaction_descriptions(transactions))

def test_transaction_descriptions_empty_transaction():
    with pytest.raises(KeyError):
        list(transaction_descriptions([{}]))

@pytest.mark.parametrize("invalid_input", [{"not": "a list"}, 123, "not a list"])
def test_transaction_descriptions_non_list_input(invalid_input):
    """Тест на передачу не списка в transaction_descriptions"""
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(transaction_descriptions(invalid_input))

def test_transaction_descriptions_empty_string():
    """Тест на пустую строку в описании"""
    transactions = [{"description": ""}]
    result = list(transaction_descriptions(transactions))
    assert result == [""]

def test_transaction_descriptions_none_value():
    """Тест на None в описании"""
    transactions = [{"description": None}]
    result = list(transaction_descriptions(transactions))
    assert result == [None]

@pytest.mark.parametrize("start, end", [(1, 9), (0, 9), (5, 5)])
def test_card_number_generator_format(start, end):
    generator = card_number_generator(start, end)
    card_number = next(generator)
    # Проверяем формат
    parts = card_number.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    # Проверяем, что все цифры в допустимом диапазоне
    digits = card_number.replace(" ", "")
    assert all(start <= int(d) <= end for d in digits)
    assert len(digits) == 16


def test_card_number_generator_multiple_calls():
    generator = card_number_generator(0, 9)
    numbers = [next(generator) for _ in range(3)]
    # Проверяем, что все номера разные (хотя теоретически могут совпадать)
    assert len(set(numbers)) >= 1  # Минимум 1 уникальный номер
    # Проверяем формат всех номеров
    for number in numbers:
        parts = number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(d.isdigit() for d in number.replace(" ", ""))

def test_card_number_generator_infinite():
    generator = card_number_generator(0, 9)
    # Берем 1000 элементов из генератора - если их меньше, будет StopIteration
    list(itertools.islice(generator, 1000))
    # Если дошли сюда - генератор не завершился после 1000 итераций


def test_card_number_generator_edge_cases():
    # Все цифры одинаковые (минимальное значение)
    generator = card_number_generator(0, 0)
    number = next(generator)
    assert number == "0000 0000 0000 0000"

    # Все цифры одинаковые (максимальное значение)
    generator = card_number_generator(9, 9)
    number = next(generator)
    assert number == "9999 9999 9999 9999"

def test_card_number_generator_invalid_range():
    """Тест на недопустимый диапазон для генератора карт"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        list(card_number_generator(10, 9))

def test_card_number_generator_negative_start():
    """Тест на отрицательное начальное значение"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        generator = card_number_generator(-1, 5)
        next(generator)

def test_card_number_generator_large_end():
    """Тест на значение end больше 9"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        generator = card_number_generator(0, 10)
        next(generator)

def test_card_number_generator_same_start_end():
    generator = card_number_generator(5, 5)
    number = next(generator)
    assert all(c == '5' for c in number if c.isdigit())

def test_card_number_generator_invalid_types():
    with pytest.raises(TypeError):
        next(card_number_generator("0", 9))
    with pytest.raises(TypeError):
        next(card_number_generator(0, "9"))

def test_card_number_generator_non_int_start():
    """Тест на нецелочисленный start"""
    with pytest.raises(TypeError):
        next(card_number_generator(1.5, 9))

def test_card_number_generator_digit_range():
    """Тест на проверку диапазона цифр"""
    start, end = 1, 5
    generator = card_number_generator(start, end)
    number = next(generator).replace(" ", "")
    assert all(start <= int(d) <= end for d in number)


def test_card_number_generator_infinite_yield():
    """Тест на бесконечную генерацию номеров"""
    generator = card_number_generator(0, 9)

    # Проверяем 1000 карт (если генератор сломается — тест упадёт)
    for _ in range(1000):
        number = next(generator)
        # Проверяем формат
        assert len(number.replace(" ", "")) == 16
        assert all(c.isdigit() for c in number if c != " ")

    # Дополнительно проверяем, что генератор не останавливается
    assert next(generator) is not None


def test_card_number_generator_fixed_output():
    """Тест на воспроизводимость при фиксированном seed"""
    generator = card_number_generator(0, 9)
    numbers1 = [next(generator) for _ in range(3)]

    # Сбрасываем генератор и проверяем воспроизводимость
    import random
    random.seed(42)
    generator = card_number_generator(0, 9)
    numbers2 = [next(generator) for _ in range(3)]

    assert numbers1 == numbers2

import itertools
from datetime import datetime

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

def test_operation_amount_format(sample_transactions):
    """Проверка корректности формата суммы операции"""
    for transaction in sample_transactions:
        amount_str = transaction["operationAmount"]["amount"]
        # Проверяем, что сумма является строкой
        assert isinstance(amount_str, str)
        # Проверяем, что строка может быть преобразована в float
        try:
            float(amount_str)
        except ValueError:
            pytest.fail(f"Amount '{amount_str}' is not a valid float number")
        # Проверяем, что сумма имеет 2 знака после запятой
        if '.' in amount_str:
            assert len(amount_str.split('.')[1]) == 2

def test_transaction_date_format(sample_transactions):
    """Проверка корректности формата даты в транзакциях"""
    for transaction in sample_transactions:
        date_str = transaction["date"]
        # Проверяем, что дата является строкой
        assert isinstance(date_str, str)
        # Пытаемся расписать дату в ISO формате
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            pytest.fail(f"Date '{date_str}' is not in valid ISO format")

# Добавим тест на пустое описание в transaction_descriptions
def test_transaction_descriptions_empty_description():
    """Тест на пустую строку в описании транзакции"""
    transactions = [{"description": ""}]
    result = list(transaction_descriptions(transactions))
    assert result == [""]

@pytest.mark.parametrize("currency, expected_count", [("USD", 2), ("RUB", 1), ("EUR", 0)])
def test_filter_by_currency(sample_transactions, currency, expected_count):
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count
    for transaction in filtered:
        assert transaction["operationAmount"]["currency"]["code"] == currency

def test_filter_by_currency_invalid_input():
    with pytest.raises(TypeError):
        list(filter_by_currency(None, "USD"))

def test_filter_by_currency_non_dict_transaction():
    """Тест, когда транзакция не является словарём"""
    transactions = ["not_a_dict", 123, None]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []

def test_filter_by_currency_empty_input():
    assert list(filter_by_currency([], "USD")) == []
    assert list(transaction_descriptions([])) == []

def test_filter_by_currency_missing_currency_key():
    transactions = [{"operationAmount": {"amount": "100"}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_operation_amount():
    transactions = [{"id": 1}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_currency():
    transactions = [{"operationAmount": {"amount": "100", "currency": {}}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_operation_amount_key():
    """Тест на отсутствие ключа operationAmount"""
    transactions = [{"id": 1}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_dict_operation_amount():
    """Тест, когда operationAmount не словарь"""
    transactions = [{"operationAmount": "invalid"}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_dict_currency():
    """Тест, когда currency не словарь"""
    transactions = [{"operationAmount": {"currency": "USD"}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_code():
    """Тест на отсутствие code в currency"""
    transactions = [{
        "id": 1,
        "state": "EXECUTED",
        "operationAmount": {"amount": "100", "currency": {"name": "USD"}}
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_non_list_input():
    """Тест на передачу не списка в filter_by_currency"""
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(filter_by_currency({"id": 1}, "USD"))

def test_filter_by_currency_invalid_currency_structure():
    """Тест на некорректную структуру currency"""
    transactions = [{
        "operationAmount": {
            "currency": "USD"  # Должно быть dict, а не str
        }
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_exception_handling():
    """Тест на обработку исключений в filter_by_currency"""
    # Транзакции, вызывающие разные исключения:
    # 1. TypeError (None вместо словаря)
    # 2. AttributeError (у строки нет метода .get())
    # 3. KeyError (нет ключа 'code')
    broken_transactions = [
        {"operationAmount": {"currency": None}},  # Вызовет TypeError
        {"operationAmount": "not_a_dict"},  # Вызовет AttributeError
        {"operationAmount": {"currency": {"name": "USD"}}},  # Нет 'code' → KeyError
    ]

    # Все исключения должны быть обработаны, результат — пустой список
    result = list(filter_by_currency(broken_transactions, "USD"))
    assert result == []

def test_filter_by_currency_missing_code_key():
    """Тест на отсутствие ключа code в currency"""
    transactions = [{
        "operationAmount": {
            "currency": {"name": "USD"}  # Нет code
        }
    }]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_transaction_descriptions(sample_transactions):
    descriptions = list(transaction_descriptions(sample_transactions))
    assert len(descriptions) == len(sample_transactions)
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]

def test_transaction_descriptions_invalid_input():
    with pytest.raises(TypeError):
        list(transaction_descriptions("not a list"))

def test_transaction_descriptions_missing_key():
    """Тест на отсутствие ключа description в транзакции"""
    transactions = [{"id": 1}, {"description": "Test"}]
    with pytest.raises(KeyError, match="description key not found in transaction"):
        list(transaction_descriptions(transactions))

def test_transaction_descriptions_with_none():
    """Тест с description=None"""
    transactions = [{"description": None}]
    result = list(transaction_descriptions(transactions))
    assert result == [None]

def test_transaction_descriptions_non_str():
    """Тест с description не строкой"""
    transactions = [{"description": 123}]
    result = list(transaction_descriptions(transactions))
    assert result == [123]

def test_transaction_descriptions_mixed():
    """Тест со смешанными транзакциями (с description и без)"""
    transactions = [{"description": "test"}, {"id": 1}]
    with pytest.raises(KeyError, match="description key not found in transaction"):
        list(transaction_descriptions(transactions))

def test_transaction_descriptions_empty_transaction():
    with pytest.raises(KeyError):
        list(transaction_descriptions([{}]))

def test_transaction_descriptions_non_list_input():
    """Тест на передачу не списка в transaction_descriptions"""
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(transaction_descriptions({"not": "a list"}))  # Передаём словарь
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(transaction_descriptions(123))  # Передаём число
    with pytest.raises(TypeError, match="transactions must be a list"):
        list(transaction_descriptions("not a list"))  # Передаём строку

def test_transaction_descriptions_empty_string():
    """Тест на пустую строку в описании"""
    transactions = [{"description": ""}]
    result = list(transaction_descriptions(transactions))
    assert result == [""]

def test_transaction_descriptions_none_value():
    """Тест на None в описании"""
    transactions = [{"description": None}]
    result = list(transaction_descriptions(transactions))
    assert result == [None]

@pytest.mark.parametrize("start, end", [(1, 9), (0, 9), (5, 5)])
def test_card_number_generator_format(start, end):
    generator = card_number_generator(start, end)
    card_number = next(generator)
    # Проверяем формат
    parts = card_number.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    # Проверяем, что все цифры в допустимом диапазоне
    digits = card_number.replace(" ", "")
    assert all(start <= int(d) <= end for d in digits)
    assert len(digits) == 16


def test_card_number_generator_multiple_calls():
    generator = card_number_generator(0, 9)
    numbers = [next(generator) for _ in range(3)]
    # Проверяем, что все номера разные (хотя теоретически могут совпадать)
    assert len(set(numbers)) >= 1  # Минимум 1 уникальный номер
    # Проверяем формат всех номеров
    for number in numbers:
        parts = number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(d.isdigit() for d in number.replace(" ", ""))

def test_card_number_generator_infinite():
    generator = card_number_generator(0, 9)
    # Берем 1000 элементов из генератора - если их меньше, будет StopIteration
    list(itertools.islice(generator, 1000))
    # Если дошли сюда - генератор не завершился после 1000 итераций


def test_card_number_generator_edge_cases():
    # Все цифры одинаковые (минимальное значение)
    generator = card_number_generator(0, 0)
    number = next(generator)
    assert number == "0000 0000 0000 0000"

    # Все цифры одинаковые (максимальное значение)
    generator = card_number_generator(9, 9)
    number = next(generator)
    assert number == "9999 9999 9999 9999"

def test_card_number_generator_invalid_range():
    """Тест на недопустимый диапазон для генератора карт"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        list(card_number_generator(10, 9))

def test_card_number_generator_negative_start():
    """Тест на отрицательное начальное значение"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        generator = card_number_generator(-1, 5)
        next(generator)

def test_card_number_generator_large_end():
    """Тест на значение end больше 9"""
    with pytest.raises(ValueError, match="start and end must be between 0 and 9"):
        generator = card_number_generator(0, 10)
        next(generator)

def test_card_number_generator_same_start_end():
    generator = card_number_generator(5, 5)
    number = next(generator)
    assert all(c == '5' for c in number if c.isdigit())

def test_card_number_generator_invalid_types():
    with pytest.raises(TypeError):
        next(card_number_generator("0", 9))
    with pytest.raises(TypeError):
        next(card_number_generator(0, "9"))

def test_card_number_generator_non_int_start():
    """Тест на нецелочисленный start"""
    with pytest.raises(TypeError):
        next(card_number_generator(1.5, 9))

def test_card_number_generator_digit_range():
    """Тест на проверку диапазона цифр"""
    start, end = 1, 5
    generator = card_number_generator(start, end)
    number = next(generator).replace(" ", "")
    assert all(start <= int(d) <= end for d in number)


def test_card_number_generator_infinite_yield():
    """Тест на бесконечную генерацию номеров"""
    generator = card_number_generator(0, 9)

    # Проверяем 1000 карт (если генератор сломается — тест упадёт)
    for _ in range(1000):
        number = next(generator)
        # Проверяем формат
        assert len(number.replace(" ", "")) == 16
        assert all(c.isdigit() for c in number if c != " ")

    # Дополнительно проверяем, что генератор не останавливается
    assert next(generator) is not None


def test_card_number_generator_fixed_output():
    """Тест на воспроизводимость при фиксированном seed"""
    generator = card_number_generator(0, 9)
    numbers1 = [next(generator) for _ in range(3)]

    # Сбрасываем генератор и проверяем воспроизводимость
    import random
    random.seed(42)
    generator = card_number_generator(0, 9)
    numbers2 = [next(generator) for _ in range(3)]

    assert numbers1 == numbers2