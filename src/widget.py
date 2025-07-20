import datetime

def mask_account_card(card_number_account: str) -> str:
    """Маскирует номер карты/счета оставляя с 7й по 12ю
     цифры  невидимыми для карты и оставляя последние
      4 цифры видимыми для счета.
      Формат маски для карты: XXXX XX** **** XXXX
      Формат маски для счета: **XXXX"""

    card_str = str(card_number_account)
    # из строки делаем список и разделяем по пробелам

    sep_card_str = card_str.split()
    # наименование карты или счет объединяем в одну строку в переменной
    name_card = " ".join(sep_card_str[:-1])
    # цифры номера карты/счета записываем в отдельную переменную
    number_card_account = sep_card_str[-1]
    if number_card_account.isdigit():
        pass
    else:
        return "Номер счета/карты должен содержать только цифры"



    # Вывод маски карты/счета + проверка на количество цифр
    if len(number_card_account) == 16:
        if name_card == 'Счет' or name_card == 'счет':
            mask_format_for_card_account = f"Счет содержит больше 16 цифр"
        else:
            mask_format_for_card_account = f"{name_card} {number_card_account[4:6]}** **** {number_card_account[12:16]}"
    elif len(number_card_account) == 20:
        if name_card == 'Счет' or name_card == 'счет':
            mask_format_for_card_account = f"{name_card} **{number_card_account[-4:]}"
        else:
            mask_format_for_card_account = f"Номер карты содержит 16 цифр"
    else:
        mask_format_for_card_account = "Номер карты/счета должен содержать 16 или 20 цифр"

    return mask_format_for_card_account


if __name__ == "__main__":
    print(mask_account_card('Счет 12341234123412341234'))


def get_date(get_data: str) -> str:
    """"Функция принимает строку и выдает дату в формате ДД.ММ.ГГГГ"""


    # разделяем по границе буквы T и берем первую часть цифр с датой
    data_info1 = get_data.split("T")[0]

    if "-" in data_info1:
        # делим цифры по знаку "-" на день, месяц и год
        year, month, day = data_info1.split("-")
    else:
        return "Нарушен формат даты, введите корректное значение, разделяя через '-' ГГГГ-ММ-ДД"



    return f"{day}.{month}.{year}"


if __name__ == "__main__":
    print(get_date(""))
