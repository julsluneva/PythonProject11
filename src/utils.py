import json
import os
from typing import List, Dict, Any

def read_operations_json() -> List[Dict[Any, Any]]:
    """Функция для чтения json-файла из директории data в папке operation.json"""

    file_path = os.path.join('..', '..', 'data', 'operation.json')

    try:
        if not os.path.isfile(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []
    except Exception:
        return []

