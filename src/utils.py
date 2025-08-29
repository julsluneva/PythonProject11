import json
import os
import logging
from typing import Any, Dict, List

# Создание и настройка логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем file handler
file_handler = logging.FileHandler('utils_module.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем formatter
file_formatter = logging.Formatter(
   ' %(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H-%M-%S'
)

# Установка formatter для handler и добавление к logger
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_operations_json() -> List[Dict[Any, Any]]:
    """Функция для чтения json-файла из директории data в папке operation.json"""

    file_path = os.path.join("..", "..", "data", "operation.json")

    try:
        logger.debug(f'Попытка чтения файла: {file_path}')
        if not os.path.isfile(file_path):
            logger.warning(f'Файл не найден: {file_path}')
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug(f'Файл успешно прочитан: {file_path}')

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                logger.error(f'Некорректный формат данных в файле {file_path}')
                return []
    except FileNotFoundError:
        logger.error(f'Файл {file_path} не найден')
        return []
    except json.JSONDecodeError as e:
        logger.error(f'Ошибка декодирования JSON в файле {file_path}: {str(e)}')
        return []
    except PermissionError as e:
        logger.error(f'Ошибка доступа к файлу {file_path}: {str(e)}')
        return []
    except Exception as e:
        logger.error(f'Неожиданная ошибка при чтении файла {file_path}: {str(e)}')
        return []
