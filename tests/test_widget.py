import pytest
from src.widget import  mask_account_card
from src.widget import get_date


@pytest.fixture()
def test_mask_account_card():
    pass


@pytest.mark.parametrize("card_number_or_account_number, expected",
                         [("MasterCard 1234123412341234", "MasterCard 12** **** 1234"),
                          ("Счет 1234123412341234", "Счет 12** **** 1234"),
                          ("Visa 1234123412341234123",
                           "Номер карты/счета должен содержать 16 или 20 цифр")

]

