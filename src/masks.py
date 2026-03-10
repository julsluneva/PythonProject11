import logging
from pathlib import Path

project_root = Path(__file__).parent.parent
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

# Создание логера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание file handler для логера
log_file_path = logs_dir / "masks.log"
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создание file formatter
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H-%M-%S")

# Установка форматтера для file_handler и добавление handler к логеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

#print(f"Логи будут записываться в: {log_file_path.absolute()}")


def get_mask_card_number(card_number: str | int) -> str:
    """Маскирует номер карты, оставляя с 7й по 12ю цифры невидимыми.
    Формат маски: XXXX XX** **** XXXX"""

    try:
        if isinstance(card_number, str):
            if not card_number.isdigit():
                error_message = "Номер карты должен содержать только цифры"
                logger.error(error_message)
                raise ValueError(error_message)
            card_str = card_number
        else:
            card_str = str(card_number)

        if len(card_str) != 16:
            error_message = "Номер карты должен содержать 16 цифр"
            logger.error(error_message)
            raise ValueError(error_message)

        masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[12:]}"
        logger.info(f"Успешное маскирование номера карты: {masked_number}")
        return masked_number
    except Exception as e:
        logger.exception(f"Ошибка при маскировании номера карты: {e}")
        raise


def get_mask_account(account_number: str | int) -> str:
    """ " Маскирует номер счета, делая видимыми последние 4 цифры"""

    try:
        if isinstance(account_number, str):
            if not account_number.isdigit():
                error_message = "Номер счета должен содержать только цифры"
                logger.error(error_message)
                raise ValueError(error_message)
            account_code = account_number
        else:
            account_code = str(account_number)

        # проверка номера счета на количество цифр
        if len(account_code) < 6:
            error_message = "Номер счета должен быть не менее 6 цифр"
            logger.error(error_message)
            raise ValueError(error_message)

        # пишем f-строку в формате маски

        mask_format_for_account = f"**{account_code[-4:]}"
        logger.info(f"Успешное маскирование номера счета: {mask_format_for_account}")
        return mask_format_for_account
    except Exception as e:
        logger.exception(f"Ошибка при маскировании счета: {e}")
        raise


if __name__ == "__main__":
    # Тестирование функций с логированием
    try:
        result1 = get_mask_card_number("1234567890123456")
        result2 = get_mask_account(12341234)
        print(result1)
        print(result2)
        if log_file_path.exists():
            print(f"Файл логов создан: {log_file_path}")
        else:
            print("Файл логов не создан!")

    except Exception as e:
        logger.exception(f"Произошла ошибка: {e}")
