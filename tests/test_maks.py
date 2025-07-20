import pytest

from src.masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number():
    masked = get_mask_card_number("1234567890123456")
    assert len(masked.replace(" ", "")) == 16
    assert "****" in masked
    assert masked.startswith("1234 56")
    assert masked.endswith("3456")


@pytest.mark.parametrize("card_number, expected", [("1234567890123456", "1234 56** **** 3456"),
                                                   ("9999888877776666", "9999 88** **** 6666"),
                                                   ("1515262612126161", "1515 26** **** 6161")])
def test_valid_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected

def test_card_number_too_long():
    # Проверка слишком длинного номера
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number("12345678901234567")

def test_card_number_with_spaces():
    # Проверка обработки строки с пробелами (должна вызывать ошибку)
    with pytest.raises(ValueError, match="В номере карты должны содержаться только цифры"):
        get_mask_card_number("1234 5678 9012 3456")

def test_card_number_with_letters():
    # Проверка обработки строки с буквами
    with pytest.raises(ValueError, match="В номере карты должны содержаться только цифры"):
        get_mask_card_number("1234abcd5678efgh")

def test_empty_string():
    # Проверка пустой строки
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number("")

