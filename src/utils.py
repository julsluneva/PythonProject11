import json
import logging
import os
from typing import Any, Dict, List

logs_dir = os.path.join("..", "logs")
os.makedirs(logs_dir, exist_ok=True)

# Создание и настройка логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем file handler
log_file_path = os.path.join("..", "logs", "utils.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем formatter
file_formatter = logging.Formatter(
    " %(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H-%M-%S"
)

# Установка formatter для handler и добавление к logger
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_operations_json() -> List[Dict[Any, Any]]:
    """Функция для чтения json-файла из директории data в папке operation.json"""

    file_path = os.path.join("..", "data", "operations.json")

    try:
        logger.debug(f"Попытка чтения файла: {os.path.abspath(file_path)}")
        if not os.path.isfile(file_path):
            logger.warning(f"Файл не найден: {os.path.abspath(file_path)}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug(f"Файл успешно прочитан: {os.path.abspath(file_path)}")

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            else:
                logger.error(f"Некорректный формат данных в файле {os.path.abspath(file_path)}")
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {os.path.abspath(file_path)}: {str(e)}")
        return []
    except PermissionError as e:
        logger.error(f"Ошибка доступа к файлу {os.path.abspath(file_path)}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {os.path.abspath(file_path)}: {str(e)}")
        return []


if __name__ == "__main__":  # pragma: no cover
    file_path = os.path.join("..", "data", "operations.json")
    print(f"Ожидаемый путь: {os.path.abspath(file_path)}")
    print(f"Файл существует: {os.path.exists(file_path)}")

    logger.debug("тест DEBUG")
    logger.info("тест INFO")
    logger.warning("тест WARNING")
    logger.error("тест ERROR")

    result = read_operations_json()
    print(f"Прочитано операций: {len(result)}")

    if os.path.exists("utils_module.log"):
        with open("utils_module.log", "r", encoding="utf-8") as f:
            logs = f.read()
            print("Лог-файл создан, записи:", logs.count("\n") + 1)
    else:
        print("Лог-файл не создан")
