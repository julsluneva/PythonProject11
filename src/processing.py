"""Модуль для обработки банковских транзакций: фильтрация, сортировка и нормализация"""

import re
from typing import Dict, List, Optional, Any


def filter_by_state(bank_oper: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и возвращает список словарей,
    имеющих ключ state. По умолчанию принимается значение ключа state - EXECUTED"""

    # Проверка на пустой статус
    if not state or not isinstance(state, str) or not state.strip():
        return []

    # Приводим state к верхнему регистру для сравнения
    state_upper = state.upper()
    filtered = []

    for oper in bank_oper:
        state_value = oper.get("state")

        # Пропускаем транзакции без статуса
        if state_value is None:
            continue

        # Преобразуем значение state в строку и приводим к верхнему регистру
        state_str = str(state_value).strip().upper()

        if state_str == state_upper:
            filtered.append(oper)

    return filtered


def sort_by_date(bank_oper: list[dict], reverse: bool = True) -> list[dict]:
    """ "Функция принимает список словарей и сортирует его по ключу date(по дате).
    По умолчанию сортировка по убыванию"""

    # Фильтруем элементы, у которых есть дата
    valid_operations = [op for op in bank_oper if op.get("date")]
    return sorted(valid_operations, key=lambda x: x.get("date", ""), reverse=reverse)



def filter_by_currency(bank_oper: List[Dict], rub_only: bool = True) -> List[Dict]:
    """Фильтрует транзакции по валюте.
    Args:
        bank_oper: Список транзакций
        rub_only: Если True - только рублевые, False - все
    Returns:
        Отфильтрованный список транзакций """


def filter_by_currency(bank_oper: List[Dict], rub_only: bool = True) -> List[Dict]:
    """Фильтрует транзакции по валюте.
    Args:
        bank_oper: Список транзакций
        rub_only: Если True - только рублевые, False - все
    Returns:
        Отфильтрованный список транзакций """

    if not bank_oper or not rub_only:
        return bank_oper

    filtered = []
    for oper in bank_oper:
        is_ruble = False

        # Проверяем разные возможные структуры данных

        # Вариант 1: Прямые поля currency_name и currency_code (CSV/Excel формат)
        currency_name = oper.get('currency_name', '')
        currency_code = oper.get('currency_code', '')

        if currency_name and isinstance(currency_name, str):
            if any(rub in currency_name.lower() for rub in ['руб', 'rub', 'ruble']):
                is_ruble = True

        if currency_code and isinstance(currency_code, str):
            if any(rub in currency_code.lower() for rub in ['rub', 'rur']):
                is_ruble = True

        # Вариант 2: Вложенная структура operationAmount (JSON формат)
        amount_info = oper.get('operationAmount', {})
        if isinstance(amount_info, dict):
            currency = amount_info.get('currency', {})
            if isinstance(currency, dict):
                curr_name = currency.get('name', '')
                curr_code = currency.get('code', '')

                if curr_name and isinstance(curr_name, str):
                    if any(rub in curr_name.lower() for rub in ['руб', 'rub', 'ruble']):
                        is_ruble = True

                if curr_code and isinstance(curr_code, str):
                    if any(rub in curr_code.lower() for rub in ['rub', 'rur']):
                        is_ruble = True

        if is_ruble:
            filtered.append(oper)

    return filtered


def normalize_transaction_structure(transaction: Dict) -> Dict:
    """Приводит структуру транзакции к единому формату. На вход принимается транзакция в произвольном
    формате, на выходе транзакция в нормализованном формате."""

    normalized = transaction.copy()

    # Инициализируем поля по умолчанию, если их нет
    if 'amount' not in normalized:
        normalized['amount'] = ''
    if 'currency_name' not in normalized:
        normalized['currency_name'] = ''
    if 'currency_code' not in normalized:
        normalized['currency_code'] = ''

    # Нормализуем поля для разных форматов файлов
    if 'operationAmount' in transaction:
        # для JSON формата
        amount_info = transaction['operationAmount']
        if isinstance(amount_info, dict):
            normalized['amount'] = amount_info.get('amount', '')
            currency_info = amount_info.get('currency', {})
            if isinstance(currency_info, dict):
                normalized['currency_name'] = currency_info.get('name', '')
                normalized['currency_code'] = currency_info.get('code', '')
    elif 'amount' in transaction and 'currency_name' in transaction:
        # для CSV формата - уже есть нужные поля, ничего не делаем
        pass

    return normalized


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Ищет транзакции, в описании которых содержится заданная строка.
      Использует регулярные выражения для поиска без учета регистра."""

    if not data or not search:
        return []

    # Компилируем регулярное выражение для поиска без учета регистра
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = []

    for transaction in data:
        description = transaction.get('description', '')
        if description is not None and isinstance(description, str) and pattern.search(description):
            filtered_data.append(transaction)
        elif description is not None and not isinstance(description, str):
            #Если описание не строка, пробуем преобразовать
            try:
                desc_str = str(description)
                if pattern.search(desc_str):
                    filtered_data.append(transaction)
            except:
                pass

    return filtered_data


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям. Принимает список словарей с данными о
    банковских операциях и список названий категорий для подсчета, а возвращает словарь, где
    ключи - названия категорий, значения - количество операций"""

    if not data:
        return {category: 0 for category in categories}

    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get('description', '')
        if description is not None:
            # Преобразуем в строку, если это не строка
            if not isinstance(description, str):
                description = str(description)

            # Приводим описание к нижнему регистру для сравнения
            description_lower = description.lower()
            for category in categories:
                if category.lower() in description_lower:
                    result[category] += 1

    return result


if __name__ == "__main__":
    # Тестирование функций
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("Фильтрация по статусу CANCELED:")
    print(filter_by_state(test_data, state="CANCELED"))

    print("\nСортировка по дате (по убыванию):")
    print(sort_by_date(test_data))

    print("\nСортировка по дате (по возрастанию):")
    print(sort_by_date(test_data, reverse=False))
