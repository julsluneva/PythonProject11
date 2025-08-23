import json
from unittest.mock import mock_open, patch

from src.utils import read_operations_json


def test_file_not_extsts():
    """Тест: файл не существует"""
    with patch("os.path.isfile", return_value=False):
        result = read_operations_json()
        assert result == []


def test_empty_json_file():
    """Тест: пустой JSON файл"""
    mock_file_data = ""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_file_data)),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
    ):
        result = read_operations_json()
        assert result == []


def test_invalid_json_format():
    """Тест: невалидный JSON формат"""
    mock_file_data = "{invalid json}"
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_file_data)),
        patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)),
    ):
        result = read_operations_json()
        assert result == []


def test_valid_json_array():
    """Тест: валидный JSON массив с объектами"""
    # Готовим тестовые данные
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    # Настраиваем моки для имитации работы с файлом
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        # вызываем тестируемую функцию
        result = read_operations_json()
        # проверяем что функция возвращает ожидаемый результат
        assert result == test_data


def test_json_not_array():
    """Тест: JSON не является массивом"""
    test_data = {"id": 1, "amount": 100}
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == []


def test_json_array_with_non_objects():
    """Тест: JSON массив содержит не только объекты"""
    test_data = [{"id": 1}, "string", 123]
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == []


def test_empty_json_array():
    """Тест: пустой JSON массив"""
    test_data = []
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", mock_open()),
        patch("json.load", return_value=test_data),
    ):
        result = read_operations_json()
        assert result == test_data


def test_permission_error():
    """Тест: ошибка доступа к файлу"""
    with (
        patch("os.path.isfile", return_value=True),
        patch("builtins.open", side_effect=FileNotFoundError("File not found")),
    ):
        result = read_operations_json()
        assert result == []


def test_other_exception():
    """Тест: другие исключения"""
    with patch("os.path.isfile", return_value=True), patch("builtins.open", side_effect=Exception("Unexpected error")):
        result = read_operations_json()
        assert result == []


def test_encoding_right():
    """Тест: правильная обработка UTF-символов"""
    test_data = [{"description": "Платеж$", "amount": 100}]

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
    ):
        result = read_operations_json()
        assert result == []
