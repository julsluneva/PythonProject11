"""Модуль для форматированного вывода банковских транзакций"""

from datetime import datetime
from typing import Dict, List

from src.masks import get_mask_account, get_mask_card_number


def format_date(date_str: str) -> str:
    """Форматируем дату из ISO формата в читаемый вид. На вход приходит дата в строковом формате,
    на выходе получаем отформатированный вариант"""

    if not date_str:
        return "Дата не указана"

    try:
        # Пробуем разные форматы дат
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%d.%m.%Y")
            except ValueError:
                continue
        return date_str[:10]  # Берем первые 10 символов, если формат неизвестен
    except Exception:
        return date_str


def mask_card_or_account(number: str) -> str:
    """Маскирует номер карты или счета. На вход приходит номер, на выходе получаем маскированный вариант"""

    if not number:
        return ""

    number_str = str(number)

    # Проверяем, это карта или счет
    if "счет" in number_str.lower():
        # Это счет
        parts = number_str.split()
        if len(parts) > 1 and parts[-1].isdigit():
            account_num = parts[-1]
            try:
                masked = get_mask_account(account_num)
                return f"{' '.join(parts[:-1])} {masked}"
            except ValueError:
                # Если номер слишком короткий, возвращаем как есть
                return number_str
        return number_str
    else:
        # Это карта
        # Ищем номер карты (последняя группа цифр)
        import re

        numbers = re.findall(r"\d+", number_str)
        if numbers:
            last_number = numbers[-1]
            if len(last_number) == 16 and last_number.isdigit():
                masked = get_mask_card_number(last_number)
                # Сохраняем название карты
                card_name = " ".join(number_str.split()[:-1]) if " " in number_str else ""
                return f"{card_name} {masked}" if card_name else masked
        return number_str


def format_transaction(transaction: Dict) -> str:
    """Форматирует одну транзакцию для вывода. На вход подаются данные транзакции, на выходе отформатированная
    строка с транзакцией"""

    # Импортируем здесь, чтобы избежать циклических импортов
    from src.processing import normalize_transaction_structure

    normalized = normalize_transaction_structure(transaction)

    date = format_date(transaction.get("date", ""))
    description = transaction.get("description", "Операция")
    from_account = mask_card_or_account(transaction.get("from", ""))
    to_account = mask_card_or_account(transaction.get("to", ""))

    amount = normalized.get("amount", "0")
    currency_name = normalized.get("currency_name", "")

    # Форматируем вывод
    lines = []
    lines.append(f"{date} {description}")
    if from_account and to_account:
        lines.append(f"{from_account} -> {to_account}")
    elif from_account:
        lines.append(f"{from_account}")
    else:
        lines.append(f"{to_account}")

    lines.append(f"Сумма: {amount} {currency_name}")
    lines.append("")  # Пустая строка для разделения

    return "\n".join(lines)


def display_transactions(transactions: List[Dict]) -> None:
    """Выводит список транзакций в консоль"""

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        print(format_transaction(transaction))
        print("-" * 50)  # Добавляем разделитель для лучшей читаемости
