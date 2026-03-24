import json
import logging
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.utils import logger, read_operations_json


def test_logger_configuration():
    """Тест: проверка конфигурации логгера"""
    assert logger is not None
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.FileHandler)

    # Проверяем форматтер
    formatter = logger.handlers[0].formatter
    expected_format = " %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert formatter._fmt == expected_format
    assert formatter.datefmt == "%Y-%m-%d %H-%M-%S"


def test_log_file_path():
    """Тест: проверка пути к файлу логов"""
    from src.utils import log_file_path

    assert "logs" in str(log_file_path)
    assert "utils.log" in str(log_file_path)


def test_file_not_exists():
    """Тест: файл не существует"""
    with patch("os.path.isfile", return_value=False):
        with patch("src.utils.logger") as mock_logger:
            result = read_operations_json()
            assert result == []
            mock_logger.warning.assert_called_once()
            mock_logger.debug.assert_called_once()


def test_empty_json_file():
    """Тест: пустой JSON файл"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data="")),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_invalid_json_format():
    """Тест: невалидный JSON формат"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data="{invalid json}")),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_valid_json_array():
    """Тест: валидный JSON массив с объектами"""
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == test_data
        assert mock_logger.debug.call_count == 2


def test_json_not_array():
    """Тест: JSON не является массивом"""
    test_data = {"id": 1, "amount": 100}
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        # debug вызывается дважды (попытка чтения и успех), но потом ошибка
        assert mock_logger.debug.call_count >= 1


def test_json_array_with_non_objects():
    """Тест: JSON массив содержит не только объекты"""
    test_data = [{"id": 1}, "string", 123]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        assert mock_logger.debug.call_count >= 1


def test_empty_json_array():
    """Тест: пустой JSON массив"""
    test_data = []
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == test_data
        # debug вызывается дважды (попытка чтения и успех)
        assert mock_logger.debug.call_count == 2


def test_permission_error():
    """Тест: ошибка доступа к файлу"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=PermissionError("Permission denied")),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_file_not_found_error():
    """Тест: файл не найден (FileNotFoundError)"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=FileNotFoundError("File not found")),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_unexpected_exception():
    """Тест: другие исключения"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=Exception("Unexpected error")),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_utf8_encoding():
    """Тест: правильная обработка UTF-8 символов"""
    test_data = [{"description": "Платеж € £ ¥", "amount": 100}]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == test_data


def test_json_decode_error():
    """Тест: ошибка декодирования JSON файла"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data="invalid json")),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()


def test_large_json_file():
    """Тест: обработка большого JSON файла"""
    large_data = [{"id": i, "value": f"test_{i}"} for i in range(1000)]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=large_data),
    ):
        result = read_operations_json()
        assert len(result) == 1000
        assert result[0]["id"] == 0
        assert result[999]["id"] == 999


def test_json_with_nested_structures():
    """Тест: JSON с вложенными структурами"""
    test_data = [{"id": 1, "operation": {"amount": 100, "currency": {"name": "RUB", "code": "RUB"}}}]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == test_data
        assert result[0]["operation"]["currency"]["code"] == "RUB"


def test_json_with_special_characters():
    """Тест: JSON со специальными символами"""
    test_data = [
        {"description": "Перевод\nс новой строки"},
        {"description": "Табуляция\tтест"},
        {"description": 'Кавычки "внутри" строки'},
    ]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == test_data


def test_file_with_bom():
    """Тест: файл с BOM (Byte Order Mark)"""
    mock_file = MagicMock()
    mock_file.read.return_value = '\ufeff[{"id": 1}]'

    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", return_value=mock_file),
        patch("json.load", return_value=[{"id": 1}]),
    ):
        result = read_operations_json()
        assert result == [{"id": 1}]


def test_function_docstring():
    """Тест: наличие docstring у функции"""
    assert read_operations_json.__doc__ is not None
    assert "json-файла" in read_operations_json.__doc__


def test_return_type_is_list():
    """Тест: проверка что функция всегда возвращает список"""
    # Случай 1: файл не существует
    with patch("os.path.isfile", return_value=False):
        result = read_operations_json()
        assert isinstance(result, list)

    # Случай 2: пустой файл
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data="")),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
    ):
        result = read_operations_json()
        assert isinstance(result, list)

    # Случай 3: валидные данные
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=[{"id": 1}]),
    ):
        result = read_operations_json()
        assert isinstance(result, list)


def test_corrupted_json_structure():
    """Тест: поврежденная структура JSON (не список и не словарь)"""
    test_data = "just a string"
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called_once()
        # debug вызывается дважды (попытка чтения и успех), но потом ошибка
        assert mock_logger.debug.call_count >= 1


def test_logging_on_file_not_found():
    """Тест: проверка логирования при отсутствии файла"""
    with patch("os.path.isfile", return_value=False):
        with patch("src.utils.logger") as mock_logger:
            result = read_operations_json()
            assert result == []
            mock_logger.warning.assert_called_once()


def test_logging_on_json_error():
    """Тест: проверка логирования при ошибке JSON"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data="invalid")),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called()


def test_logging_on_permission_error():
    """Тест: проверка логирования при ошибке доступа"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=PermissionError("Access denied")),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called()


def test_logging_on_unexpected_error():
    """Тест: проверка логирования при неожиданной ошибке"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=Exception("Unexpected")),
        patch("src.utils.logger") as mock_logger,
    ):
        result = read_operations_json()
        assert result == []
        mock_logger.error.assert_called()


def test_absolute_path_construction():
    """Тест: проверка построения абсолютного пути"""
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = False
        with patch("src.utils.logger") as _:
            result = read_operations_json()
            assert result == []
            # Проверяем что isfile был вызван с правильным путем
            args = mock_isfile.call_args[0][0]
            assert "data" in args
            assert "operations.json" in args


def test_absolute_path_in_logs():
    """Тест: проверка что в логах используется абсолютный путь"""
    with patch("os.path.abspath") as mock_abspath:
        mock_abspath.return_value = "/absolute/path/to/file.json"

        with patch("os.path.isfile", return_value=False):
            with patch("src.utils.logger") as mock_logger:
                result = read_operations_json()
                assert result == []
                # Проверяем что abspath вызывался для логов
                mock_abspath.assert_called()
                mock_logger.warning.assert_called_once()


def test_successful_read_with_absolute_path():
    """Тест: успешное чтение с проверкой абсолютного пути в логах"""
    test_data = [{"id": 1, "amount": 100}]

    with patch("os.path.abspath") as mock_abspath:
        mock_abspath.return_value = "/absolute/path/to/file.json"

        with (
            patch("os.path.isfile", return_value=True),
            patch("builtins.open", mock_open()),
            patch("json.load", return_value=test_data),
            patch("src.utils.logger") as mock_logger,
        ):
            result = read_operations_json()
            assert result == test_data
            # Проверяем что debug вызывался дважды
            assert mock_logger.debug.call_count == 2


# def test_main_block_with_log_file():
#     """Тест: выполнение блока __main__ когда лог-файл существует"""
#     original_print = print
#
#     try:
#         import builtins
#         builtins.print = lambda *args, **kwargs: None
#
#         import sys
#         original_name = sys.modules["src.utils"].__name__
#
#         # Мокаем FileHandler, чтобы избежать создания реального файла
#         mock_handler = MagicMock()
#
#         with patch("os.path.abspath", return_value="C:/fake/path/operations.json"):
#             with patch("os.path.exists", side_effect=[True, True]):
#                 with patch("src.utils.read_operations_json", return_value=[{"id": 1}, {"id": 2}, {"id": 3}]):
#                     with patch("builtins.open", mock_open(read_data="line1\nline2\nline3")):
#                         with patch("logging.FileHandler", return_value=mock_handler):
#                             # Мокаем добавление handler чтобы избежать реального логирования
#                             with patch("logging.Logger.addHandler"):
#                                 # Временно меняем __name__
#                                 sys.modules["src.utils"].__name__ = "__main__"
#
#                                 try:
#                                     # Перезагружаем модуль
#                                     import importlib
#                                     importlib.reload(sys.modules["src.utils"])
#                                     assert True
#                                 except Exception as e:
#                                     pytest.fail(f"Блок __main__ вызвал ошибку: {e}")
#                                 finally:
#                                     # Восстанавливаем оригинальное имя
#                                     sys.modules["src.utils"].__name__ = original_name
#     finally:
#         builtins.print = original_print
#
#
# def test_main_block_without_log_file():
#     """Тест: выполнение блока __main__ когда лог-файл не существует"""
#     original_print = print
#
#     try:
#         import builtins
#         builtins.print = lambda *args, **kwargs: None
#
#         import sys
#         original_name = sys.modules["src.utils"].__name__
#
#         mock_handler = MagicMock()
#
#         with patch("os.path.abspath", return_value="C:/fake/path/operations.json"):
#             with patch("os.path.exists", side_effect=[True, False]):
#                 with patch("src.utils.read_operations_json", return_value=[]):
#                     with patch("logging.FileHandler", return_value=mock_handler):
#                         with patch("logging.Logger.addHandler"):
#                             sys.modules["src.utils"].__name__ = "__main__"
#
#                             try:
#                                 import importlib
#                                 importlib.reload(sys.modules["src.utils"])
#                                 assert True
#                             except Exception as e:
#                                 pytest.fail(f"Блок __main__ вызвал ошибку: {e}")
#                             finally:
#                                 sys.modules["src.utils"].__name__ = original_name
#     finally:
#         builtins.print = original_print
#
#
# # def test_main_block_no_file():
# #     """Тест: выполнение блока __main__ когда файл операций не существует"""
# #     original_print = print
# #
# #     try:
# #         import builtins
# #         builtins.print = lambda *args, **kwargs: None
# #
# #         import sys
# #         original_name = sys.modules["src.utils"].__name__
# #
# #         mock_handler = MagicMock()
# #
# #         with patch("os.path.abspath", return_value="C:/fake/path/operations.json"):
# #             with patch("os.path.exists", return_value=False):
# #                 with patch("logging.FileHandler", return_value=mock_handler):
# #                     with patch("logging.Logger.addHandler"):
# #                         sys.modules["src.utils"].__name__ = "__main__"
# #
# #                         try:
# #                             import importlib
# #                             importlib.reload(sys.modules["src.utils"])
# #                             assert True
# #                         except Exception as e:
# #                             pytest.fail(f"Блок __main__ вызвал ошибку: {e}")
# #                         finally:
# #                             sys.modules["src.utils"].__name__ = original_name
# #     finally:
# #         builtins.print = original_print

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
