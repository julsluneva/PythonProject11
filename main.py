"""Основной модуль программы для работы с банковскими транзакциями."""

import os
import sys
from typing import Dict, List

from src.display import display_transactions
from src.processing import (filter_by_currency, filter_by_state, process_bank_operations, process_bank_search,
                            sort_by_date)
from src.read_csv_excel import load_transactions_from_csv, load_transactions_from_excel

# Добавляем путь к src для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def get_file_path(filename: str) -> str:
    """Получает полный путь к файлу в папке data"""

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    return os.path.join(data_dir, filename)


def read_json_file() -> List[Dict]:
    """Читает JSON файл напрямую, используя правильный путь"""
    file_path = get_file_path("operations.json")
    try:
        import json

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                print(f"Успешно загружено {len(data)} транзакций из JSON")
                return data
            else:
                print("Ошибка: JSON файл должен содержать список")
                return []
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return []


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """Получает выбор пользователя с валидацией (на вход prompt: Текст заголовка,
    valid_choices: Список допустимых ответов, а возвращает выбор пользователя)"""

    while True:
        choice = input(prompt).strip()
        if choice.lower() in [c.lower() for c in valid_choices]:
            return choice.lower()
        print(f"Некорректный ввод. Пожалуйста, выберите из: {', '.join(valid_choices)}")


def get_status_from_user() -> str:
    """Получает от пользователя статус для фильтрации с валидацией"""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status_input = input("Статус: ").strip().upper()
        if status_input in valid_statuses:
            return status_input
        print(f'Статус операции "{status_input}" недоступен.')
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input("\nВаш выбор: ").strip()

    transactions = []

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = read_json_file()
    elif file_choice == "2":
        file_path = get_file_path("transactions.csv")
        print("Для обработки выбран CSV-файл.")
        transactions = load_transactions_from_csv(file_path)
    elif file_choice == "3":
        file_path = get_file_path("transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
        transactions = load_transactions_from_excel(file_path)
    else:
        print("Некорректный выбор. Программа завершена.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    # Диагностика: посмотрим, какие статусы есть в данных
    print(f"\nЗагружено {len(transactions)} транзакций")

    # Соберем все уникальные значения статусов
    unique_states = set()
    state_types = set()

    for i, t in enumerate(transactions[:10]):  # Смотрим первые 10 транзакций
        state = t.get("state")
        print(f"Транзакция {i+1}: state={state}, тип={type(state).__name__})")

        if state is not None:
            unique_states.add(str(state))
            state_types.add(type(state).__name__)

    print(f"\nУникальные значения статусов (первые 10): {unique_states}")
    print(f"Типы данных статусов: {state_types}")

    # Посчитаем количество каждого статуса
    from collections import Counter

    state_counter: Counter[str] = Counter()
    for t in transactions:
        state = t.get("state")
        if state is not None:
            state_counter[str(state)] += 1

    print("\nСтатистика по статусам:")
    for state, count in state_counter.most_common(10):
        print(f" {state}: {count}")

    # Фильтрация по статусу
    status = get_status_from_user()
    filtered_transactions = filter_by_state(transactions, status)
    print(f"\nОперации отфильтрованы по статусу '{status}'")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        print("\nПримеры значений статусов из данных:")
        examples = list(state_counter.keys())[:5]
        for ex in examples:
            print(
                f" '{ex}'(тип: {type(next(t['state'] for t in transactions if str(t.get('state')) == ex)).__name__})"
            )

        return

    # Сортировка по дате
    sort_choice = get_user_choice("Отсортировать операции по дате? Да/Нет: ", ["да", "нет"])

    if sort_choice == "да":
        order_choice = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию): ", ["возрастанию", "убыванию"]
        )
        reverse = order_choice == "убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)
        print(f"Операции отсортированы по дате ({'по убыванию' if reverse else 'по возрастанию'})")

    # Фильтрация по валюте
    currency_choice = get_user_choice("\nВыводить только рублевые транзакции? Да/Нет: ", ["да", "нет"])

    if currency_choice == "да":
        filtered_transactions = filter_by_currency(filtered_transactions, rub_only=True)
        print("Выводятся только рублевые транзакции")

    # Поиск по описанию
    search_choice = get_user_choice(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет: ", ["да", "нет"]
    )
    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)
            print(f"Применен фильтр по слову: {search_word}")

    # Вывод результатов
    print("\n" + "=" * 50)
    print("Распечатываю итоговый список транзакций...")
    print("=" * 50 + "\n")

    display_transactions(filtered_transactions)

    # Дополнительно: демонстрация функции подсчета по категориям
    if filtered_transactions:
        print("\n" + "=" * 50)
        print("Статистика по категориям операций:")
        categories = ["Перевод организации", "Перевод с карты на карту", "Перевод со счета на счет", "Открытие вклада"]
        category_stats = process_bank_operations(filtered_transactions, categories)
        for category, count in category_stats.items():
            if count > 0:
                print(f" {category}: {count} операций")


if __name__ == "__main__":
    main()
