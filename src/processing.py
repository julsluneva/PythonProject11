bank_oper = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(bank_oper: list[dict], state: str = "EXECUTED") -> list[dict]:
    """ "Функция принимает список словарей и возвращает список словарей,
    имеющих ключ state.По умолчанию принимается значение ключа
     state - EXECUTIVE"""

    # выводим в консоль нужный словарь
    return [bank_oper for bank_oper in bank_oper if bank_oper.get("state") == state]


if __name__ == "__main__":
    print(filter_by_state(bank_oper, state="CANCELED"))


def sort_by_date(bank_oper: list[dict], reverse=True) -> list[dict]:
    """ "Функция принимает список словарей и сортирует его по ключу date(по дате).
    По умолчанию сортировка по убыванию"""

    return sorted(bank_oper, key=lambda x: x["date"], reverse=reverse)


if __name__ == "__main__":
    print(sort_by_date(bank_oper))
