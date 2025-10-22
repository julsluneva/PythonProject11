import os
from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список  из файла в формате csv и выдает список словарей с транзакциями"""

    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict("records")
        print(f" Успешно загружено {len(transactions)} транзакций из CSV")
        return transactions  # type: ignore
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список из файла в формате Excel и выдает список словарей с транзакциями"""

    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict("records")
        print(f"Успешно загружено {len(transactions)} транзакций из Excel")
        return transactions  # type: ignore
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []


current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)

file_path_excel = os.path.join(project_root, "data", "transactions_excel.xlsx")
file_path_csv = os.path.join(project_root, "data", "transactions.csv")

transactions_excel = load_transactions_from_excel(file_path_excel)
transactions_csv = load_transactions_from_csv(file_path_csv)

print("Excel транзакции:", len(transactions_excel))
print("CSV транзакции:", len(transactions_csv))
