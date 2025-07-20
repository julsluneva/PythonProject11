def get_mask_card_number(card_number: int) -> str:
    """Маскирует номер карты, оставляя с 7й по 12ю цифры  невидимыми.
    Формат маски: XXXX XX** **** XXXX"""

    card_str = str(card_number)
    if not card_str:
        raise ValueError("Номер карты должен содержать 16 цифр")

    if not card_str.isdigit():
        raise ValueError("В номере карты должны содержаться только цифры")

    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[12:]}"


if __name__ == "__main__":
    print(get_mask_card_number(1234123412341234))


def get_mask_account(account_number: int) -> str:
    """ " Маскирует номер счета, делая видимыми последние 4 цифры"""

    account_code = str(account_number)

    # проверка номера счета на количество цифр
    if len(account_code) < 6:
        raise ValueError("Номер счета должен быть не менее 6 цифр")

    # пишем f-строку в формате маски

    mask_format_for_account = f"**{account_code[-4:]}"

    return mask_format_for_account


if __name__ == "__main__":
    print(get_mask_account(1234123412341234))
