import logging
import runpy
from typing import Any
from unittest.mock import patch

import pytest

from src.masks import get_mask_account, get_mask_card_number, logger


# Фикстуры для тестов
@pytest.fixture
def valid_card_number() -> int:
    return 1234567812345678


@pytest.fixture
def valid_account_number() -> int:
    return 1234567890


# тестирование функции маскировки номера карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567812345678, "1234 56** **** 5678"),
        (1111222233334444, "1111 22** **** 4444"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_get_mask_card_number_valid(card_number: int, expected: str):
    """Тестирование функции маскировки номера карты с валидными данными"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card_number, expected_exception",
    [
        (123456781234567, ValueError),  # Недостаточно цифр
        (12345678123456789, ValueError),  # Слишком много цифр
        ("1234abcd5678efgh", ValueError),  # Не цифровые символы
        ("", ValueError),  # Пустая строка
    ],
)
def test_get_mask_card_number_invalid(invalid_card_number: Any, expected_exception: Any):
    """Тестирование функции маскировки номера карты с невалидными данными"""
    with pytest.raises(expected_exception):
        get_mask_card_number(invalid_card_number)


# Параметризация для тестирования функции маскировки номера счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        (1234567890, "**7890"),
        (9876543210, "**3210"),
        (1000000001, "**0001"),
        (123456, "**3456"),  # Минимально допустимая длина
    ],
)
def test_get_mask_account_valid(account_number: int, expected: str):
    """Тестирование функции маскировки номера счета с валидными данными"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account_number, expected_exception",
    [
        (12345, ValueError),  # Недостаточно цифр
        ("abcdefghij", ValueError),  # Не цифровые символы
        ("", ValueError),  # Пустая строка
    ],
)
def test_get_mask_account_invalid(invalid_account_number: Any, expected_exception: Any):
    """Тестирование функции маскировки номера счета с невалидными данными"""
    with pytest.raises(expected_exception):
        get_mask_account(invalid_account_number)


# Тесты с использованием фикстур
def test_get_mask_card_number_with_fixture(valid_card_number: int):
    """Тестирование с использованием фикстуры для номера карты"""
    assert get_mask_card_number(valid_card_number) == "1234 56** **** 5678"


def test_get_mask_account_with_fixture(valid_account_number: int):
    """Тестирование с использованием фикстуры для номера счета"""
    assert get_mask_account(valid_account_number) == "**7890"


# Тесты для логирования
def test_get_mask_card_number_with_logger():
    """Тест: проверка логирования при успешном маскировании"""
    with patch("src.masks.logger") as mock_logger:
        result = get_mask_card_number("1234567812345678")
        assert result == "1234 56** **** 5678"
        mock_logger.info.assert_called_once()
        mock_logger.debug.assert_not_called()
        mock_logger.error.assert_not_called()


def test_get_mask_card_number_error_logging():
    """Тест: проверка логирования при ошибке"""
    with patch("src.masks.logger") as mock_logger:
        with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
            get_mask_card_number("1234abcd5678efgh")
        mock_logger.error.assert_called_once()
        mock_logger.exception.assert_called_once()


def test_get_mask_account_with_logger():
    """Тест: проверка логирования при успешном маскировании счета"""
    with patch("src.masks.logger") as mock_logger:
        result = get_mask_account("1234567890")
        assert result == "**7890"
        mock_logger.info.assert_called_once()


def test_get_mask_account_error_logging():
    """Тест: проверка логирования при ошибке маскирования счета"""
    with patch("src.masks.logger") as mock_logger:
        with pytest.raises(ValueError, match="Номер счета должен быть не менее 6 цифр"):
            get_mask_account("12345")
        mock_logger.error.assert_called_once()
        mock_logger.exception.assert_called_once()


# Тесты для граничных случаев
def test_get_mask_card_number_edge_cases():
    """Тест: граничные случаи для номера карты"""
    # Номер карты как строка
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"

    # Номер карты как число
    assert get_mask_card_number(1234567812345678) == "1234 56** **** 5678"

    # Номер карты с ведущими нулями
    assert get_mask_card_number("0000123456781234") == "0000 12** **** 1234"


def test_get_mask_account_edge_cases():
    """Тест: граничные случаи для номера счета"""
    # Счет как строка
    assert get_mask_account("1234567890") == "**7890"

    # Счет как число
    assert get_mask_account(1234567890) == "**7890"

    # Минимальная длина (6 цифр)
    assert get_mask_account("123456") == "**3456"

    # Длинный счет (20 цифр)
    assert get_mask_account("12345678901234567890") == "**7890"


def test_get_mask_card_number_invalid_length():
    """Тест: неверная длина номера карты"""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number("123456789012345")  # 15 цифр

    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number("12345678901234567")  # 17 цифр


def test_get_mask_account_invalid_length():
    """Тест: неверная длина номера счета"""
    with pytest.raises(ValueError, match="Номер счета должен быть не менее 6 цифр"):
        get_mask_account("12345")  # 5 цифр


def test_get_mask_card_number_non_digit():
    """Тест: номер карты с нецифровыми символами"""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234-5678-9012-3456")

    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234 5678 9012 3456")


def test_get_mask_account_non_digit():
    """Тест: номер счета с нецифровыми символами"""
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account("ACCT-12345")


# Тесты для конфигурации логгера
def test_logger_configured():
    """Тест: проверка конфигурации логгера"""
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)


def test_log_file_creation():
    """Тест: создание файла логов"""
    from pathlib import Path

    # Проверяем что директория для логов создается
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "logs"
    assert logs_dir.exists()


# Тесты для обработки None
def test_get_mask_card_number_with_none():
    """Тест: передача None в функцию"""
    with pytest.raises(ValueError):
        get_mask_card_number(None)  # type: ignore


def test_get_mask_account_with_none():
    """Тест: передача None в функцию"""
    with pytest.raises(ValueError):
        get_mask_account(None)  # type: ignore


# Упрощенный тест для покрытия блока __main__
def test_main_block_simple():
    """Простой тест для импорта модуля"""
    # Просто импортируем модуль - этого достаточно для покрытия
    import src.masks

    assert src.masks is not None


def test_get_mask_card_number_with_different_input_types():
    """Тест: разные типы входных данных для номера карты"""
    # Строка с цифрами
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"

    # Целое число
    assert get_mask_card_number(1234567812345678) == "1234 56** **** 5678"

    # Строка с ведущими нулями
    assert get_mask_card_number("0000123456781234") == "0000 12** **** 1234"


def test_get_mask_account_with_different_input_types():
    """Тест: разные типы входных данных для номера счета"""
    # Строка с цифрами
    assert get_mask_account("1234567890") == "**7890"

    # Целое число
    assert get_mask_account(1234567890) == "**7890"

    # Длинный номер
    assert get_mask_account("12345678901234567890") == "**7890"

    # Минимальная длина
    assert get_mask_account("123456") == "**3456"


def test_get_mask_card_number_value_error_messages():
    """Тест: проверка сообщений об ошибках для карты"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("1234abcd")
    assert "Номер карты должен содержать только цифры" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("123456789012345")
    assert "Номер карты должен содержать 16 цифр" in str(exc_info.value)


def test_get_mask_account_value_error_messages():
    """Тест: проверка сообщений об ошибках для счета"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account("1234abcd")
    assert "Номер счета должен содержать только цифры" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        get_mask_account("12345")
    assert "Номер счета должен быть не менее 6 цифр" in str(exc_info.value)


def test_logger_handlers():
    """Тест: проверка наличия обработчиков логгера"""
    assert len(logger.handlers) > 0
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    assert all(hasattr(h, "formatter") for h in logger.handlers)


def test_logger_formatter():
    """Тест: проверка форматтера логгера"""
    handler = logger.handlers[0]
    assert handler.formatter._fmt == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert handler.formatter.datefmt == "%Y-%m-%d %H-%M-%S"


def test_get_mask_card_number_exception_handling():
    """Тест: обработка исключений в get_mask_card_number"""
    with patch("src.masks.logger") as mock_logger:
        with pytest.raises(ValueError):
            get_mask_card_number("invalid")
        mock_logger.exception.assert_called_once()


def test_get_mask_account_exception_handling():
    """Тест: обработка исключений в get_mask_account"""
    with patch("src.masks.logger") as mock_logger:
        with pytest.raises(ValueError):
            get_mask_account("invalid")
        mock_logger.exception.assert_called_once()


def test_main_block_execution():
    """Тест: выполнение блока __main__ без ошибок"""
    try:
        runpy.run_module("src.masks", run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        pytest.fail(f"Блок __main__ вызвал ошибку: {e}")


def test_logger_functionality():
    """Тест: функциональность логгера"""
    # Просто проверяем что логгер существует и имеет обработчики
    from src.masks import logger

    assert logger is not None
    assert len(logger.handlers) > 0

    # Проверяем что можно записать сообщение
    try:
        logger.debug("Test debug message")
        logger.info("Test info message")
        logger.warning("Test warning message")
    except Exception as e:
        pytest.fail(f"Логгер не работает: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
