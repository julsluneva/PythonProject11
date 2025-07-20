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

