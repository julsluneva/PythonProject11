
from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список  из файла в формате csv и выдает список словарей с транзакциями"""

    try:
        df = pd.read_csv(file_path, delimiter=';') # Явно указываем разделитель
        #print(f"Колонки в CSV файле: {list(df.columns)}") # Диагностика

        # Преобразуем в список словарей
        transactions = df.to_dict("records")

        # Нормализуем ключи (приводим к нижнему регистру для единообразия)
        normalized_transactions = []
        for trans in transactions:
            normalized = {}
            for key, value in trans.items():
                # Преобразуем ключ в строку, затем применяем lower
                normalized_key = str(key).lower().strip()
                normalized[normalized_key] = value
            normalized_transactions.append(normalized)

        print(f"Успешно загружено {len(normalized_transactions)} транзакций из CSV")
        return normalized_transactions

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
        #print(f"Колонки в Excel файле: {list(df.columns)}") # Диагностика

        transactions = df.to_dict("records")

        #Нормализуем ключи (приводим к нижнему регистру для единообразия)
        normalized_transactions = []
        for trans in transactions:
            normalized = {}
            for key, value in trans.items():
                # Приводим ключи к нижнему регистру и убираем пробелы
                normalized_key = str(key).lower().strip()
                normalized[normalized_key] = value
            normalized_transactions.append(normalized)

        print(f"Успешно загружено {len(normalized_transactions)} транзакций из Excel")
        return normalized_transactions

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []


# current_dir = os.path.dirname(__file__)
# project_root = os.path.dirname(current_dir)
#
# file_path_excel = os.path.join(project_root, "data", "transactions_excel.xlsx")
# file_path_csv = os.path.join(project_root, "data", "transactions.csv")
#
# transactions_excel = load_transactions_from_excel(file_path_excel)
# transactions_csv = load_transactions_from_csv(file_path_csv)
#
#
#
# if __name__ == "__main__":
#     print("Excel транзакции:", len(transactions_excel))
#     print("CSV транзакции:", len(transactions_csv))

