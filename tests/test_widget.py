import pytest

from src.widget import get_date, mask_account_card


# Фикстуры для функции mask_account_card
@pytest.fixture
def valid_card_number():
    return "Visa Platinum 1234567890123456"


@pytest.fixture
def valid_account_number():
    return "Счет 12345678901234567890"


@pytest.fixture
def invalid_number_letters():
    return "Visa Gold 1234abcd56789012"


@pytest.fixture
def invalid_number_short():
    return "Mastercard 12345678"


# Фикстуры для функции get_date
@pytest.fixture
def valid_date_string():
    return "2023-04-15T12:30:45"


@pytest.fixture
def invalid_date_string():
    return "2023/04/15T12:30:45"


@pytest.fixture
def empty_date_string():
    return ""


# Параметризованные тесты для mask_account_card
@pytest.mark.parametrize(
    "input_number, expected",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 56** **** 3456"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Maestro 1234567890123456", "Maestro 56** **** 3456"),
        ("счет 12345678901234567890", "счет **7890"),
    ],
)
def test_mask_account_card_valid(input_number, expected):
    assert mask_account_card(input_number) == expected


@pytest.mark.parametrize(
    "input_number, expected",
    [
        ("Visa Gold 1234abcd56789012", "Номер счета/карты должен содержать только цифры"),
        ("Mastercard 12345678", "Номер карты/счета должен содержать 16 или 20 цифр"),
        ("Счет 1234567890", "Номер карты/счета должен содержать 16 или 20 цифр"),
    ],
)
def test_mask_account_card_invalid(input_number, expected):
    assert mask_account_card(input_number) == expected


# Параметризованные тесты для get_date
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023-04-15T12:30:45", "15.04.2023"),
        ("1999-12-31T23:59:59", "31.12.1999"),
        ("2000-01-01T00:00:00", "01.01.2000"),
    ],
)
def test_get_date_valid(input_date, expected):
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023/04/15T12:30:45", "Нарушен формат даты, введите корректное значение, разделяя через '-' ГГГГ-ММ-ДД"),
        ("", "Нарушен формат даты, введите корректное значение, разделяя через '-' ГГГГ-ММ-ДД"),
        ("15-04-2023T12:30:45", "Нарушен формат даты, введите корректное значение, разделяя через '-' ГГГГ-ММ-ДД"),
    ],
)
def test_get_date_invalid(input_date, expected):
    assert get_date(input_date) == expected


# Тесты с использованием фикстур
def test_mask_account_card_with_fixtures(
    valid_card_number, valid_account_number, invalid_number_letters, invalid_number_short
):
    assert mask_account_card(valid_card_number) == "Visa Platinum 56** **** 3456"
    assert mask_account_card(valid_account_number) == "Счет **7890"
    assert mask_account_card(invalid_number_letters) == "Номер счета/карты должен содержать только цифры"
    assert mask_account_card(invalid_number_short) == "Номер карты/счета должен содержать 16 или 20 цифр"


def test_get_date_with_fixtures(valid_date_string, invalid_date_string, empty_date_string):
    assert get_date(valid_date_string) == "15.04.2023"
    assert get_date(invalid_date_string) == (
        "Нарушен формат даты, введите корректное значение," " разделяя через '-' ГГГГ-ММ-ДД"
    )
    assert get_date(empty_date_string) == (
        "Нарушен формат даты, введите корректное значение," " разделяя через '-' ГГГГ-ММ-ДД"
    )
