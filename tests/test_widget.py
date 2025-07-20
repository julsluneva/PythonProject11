import pytest
from src.widget import  mask_account_card
from src.widget import get_date





@pytest.mark.parametrize("card_number_or_account_number, expected",
                         [("MasterCard 1234123412341234", "MasterCard 12** **** 1234"),
                          ("Счет 1234123412341234", "Счет содержит больше 16 цифр"),
                          ("Visa 1234123412341234123",
                           "Номер карты/счета должен содержать 16 или 20 цифр"),
                          ("Visa 123412341234/)34", "Номер счета/карты должен содержать только цифры"),
                          ("Счет 12341234123412341234", "Счет **1234")


])
def test_mask_account_card(card_number_or_account_number, expected):
    assert mask_account_card(card_number_or_account_number) == expected



@pytest.mark.parametrize("iso_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2025-12-31T23:59:59.999999", "31.12.2025"),
    ("2000-01-01T00:00:00.000000", "01.01.2000"),])
def test_get_date(iso_date, expected):
    assert get_date(iso_date) == expected

def test_invalid_get_date():
    with pytest.raises(ValueError):
        get_date("Нарушен формат даты, введите корректное значение, разделяя через '-' ГГГГ-ММ-ДД")

