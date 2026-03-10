
import os
import sys
from unittest.mock import patch, MagicMock

import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from src.read_csv_excel import load_transactions_from_csv, load_transactions_from_excel


# Тесты для CSV
@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_success(mock_read_csv):
    """Тест успешной загрузки транзакций из CSV"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        mock_read_csv.return_value = mock_df
        file_path = "test.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        mock_read_csv.assert_called_once_with(file_path, delimiter=';')
        mock_df.to_dict.assert_called_once_with("records")
        assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        mock_print.assert_called_once_with("Успешно загружено 2 транзакций из CSV")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_file_not_found(mock_read_csv):
    """Тест обработки ошибки FileNotFoundError для CSV"""
    mock_read_csv.side_effect = FileNotFoundError("File not found")
    file_path = "nonexistent.csv"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_csv(file_path)

        mock_read_csv.assert_called_once_with(file_path, delimiter=';')
        assert result == []
        mock_print.assert_called_once_with("Ошибка: Файл nonexistent.csv не найден")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_general_error(mock_read_csv):
    """Тест для обработки общей ошибки для CSV"""
    mock_read_csv.side_effect = Exception("Some error")
    file_path = "corrupted.csv"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_csv(file_path)

    mock_read_csv.assert_called_once_with(file_path, delimiter=';')
    assert result == []
    mock_print.assert_called_once_with("Ошибка при чтении CSV файла: Some error")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_empty_file(mock_read_csv):
    """Тест загрузки пустого CSV файла"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = []
        mock_read_csv.return_value = mock_df
        file_path = "empty.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        mock_read_csv.assert_called_once_with(file_path, delimiter=';')
        mock_df.to_dict.assert_called_once_with("records")
        assert result == []
        mock_print.assert_called_once_with("Успешно загружено 0 транзакций из CSV")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_single_transaction(mock_read_csv):
    """Тест загрузки CSV с одной транзакцией"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
        mock_read_csv.return_value = mock_df
        file_path = "single.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        mock_read_csv.assert_called_once_with(file_path, delimiter=';')
        mock_df.to_dict.assert_called_once_with("records")
        assert result == [{"id": 1, "amount": 100}]
        mock_print.assert_called_once_with("Успешно загружено 1 транзакций из CSV")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_specific_exception(mock_read_csv):
    """Тест обработки конкретных исключений для CSV"""
    test_cases = [
        (PermissionError("Permission denied"), "Permission denied"),
        (IsADirectoryError("Is a directory"), "Is a directory"),
        (Exception("Unicode decode error"), "Unicode decode error"),
    ]
    for exception, expected_message in test_cases:
        mock_read_csv.side_effect = exception
        file_path = "test.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        assert result == []
        mock_read_csv.assert_called_with(file_path, delimiter=';')
        mock_print.assert_called_once_with(f"Ошибка при чтении CSV файла: {expected_message}")
        mock_read_csv.reset_mock()


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_with_none_dataframe(mock_read_csv):
    """Тест, когда pd.read_csv возвращает None"""
    mock_read_csv.return_value = None
    file_path = "test.csv"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_csv(file_path)

    mock_read_csv.assert_called_once_with(file_path, delimiter=';')
    assert result == []
    mock_print.assert_called_once()


@patch("read_csv_excel.pd.read_csv")
def test_transactions_from_csv_empty_string_file_path(mock_read_csv):
    """Тест с пустым путем к файлу для CSV"""
    mock_read_csv.side_effect = FileNotFoundError()
    file_path = ""

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_csv(file_path)

    mock_read_csv.assert_called_once_with(file_path, delimiter=';')
    assert result == []
    mock_print.assert_called_once_with("Ошибка: Файл  не найден")


# Тесты для Excel
@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_success(mock_read_excel):
    """Тест успешной загрузки транзакций из Excel"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [{"id": 1, "amount": 150}, {"id": 2, "amount": 250}]
        mock_read_excel.return_value = mock_df
        file_path = "test.xlsx"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_excel(file_path)

        mock_read_excel.assert_called_once_with(file_path)
        mock_df.to_dict.assert_called_once_with("records")
        assert result == [{"id": 1, "amount": 150}, {"id": 2, "amount": 250}]
        mock_print.assert_called_once_with("Успешно загружено 2 транзакций из Excel")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_file_not_found(mock_read_excel):
    """Тест обработки ошибки FileNotFoundError для Excel"""
    mock_read_excel.side_effect = FileNotFoundError("Excel file not found")
    file_path = "nonexistent.xlsx"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_excel(file_path)

        mock_read_excel.assert_called_once_with(file_path)
        assert result == []
        mock_print.assert_called_once_with("Ошибка: Файл nonexistent.xlsx не найден")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_general_error(mock_read_excel):
    """Тест для обработки общей ошибки для Excel"""
    mock_read_excel.side_effect = Exception("Excel read error")
    file_path = "corrupted.xlsx"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_excel(file_path)

    mock_read_excel.assert_called_once_with(file_path)
    assert result == []
    mock_print.assert_called_once_with("Ошибка при чтении Excel файла: Excel read error")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_empty_file(mock_read_excel):
    """Тест загрузки пустого Excel файла"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = []
        mock_read_excel.return_value = mock_df
        file_path = "empty.xlsx"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_excel(file_path)

        mock_read_excel.assert_called_once_with(file_path)
        mock_df.to_dict.assert_called_once_with("records")
        assert result == []
        mock_print.assert_called_once_with("Успешно загружено 0 транзакций из Excel")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_single_transaction(mock_read_excel):
    """Тест загрузки Excel с одной транзакцией"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [{"id": 1, "amount": 150}]
        mock_read_excel.return_value = mock_df
        file_path = "single.xlsx"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_excel(file_path)

        mock_read_excel.assert_called_once_with(file_path)
        mock_df.to_dict.assert_called_once_with("records")
        assert result == [{"id": 1, "amount": 150}]
        mock_print.assert_called_once_with("Успешно загружено 1 транзакций из Excel")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_specific_exception(mock_read_excel):
    """Тест обработки конкретных исключений для Excel"""
    test_cases = [
        (PermissionError("Permission denied"), "Permission denied"),
        (ValueError("Unsupported format"), "Unsupported format"),
    ]

    for exception, expected_message in test_cases:
        mock_read_excel.side_effect = exception
        file_path = "test.xlsx"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_excel(file_path)

        assert result == []
        mock_read_excel.assert_called_with(file_path)
        mock_print.assert_called_once_with(f"Ошибка при чтении Excel файла: {expected_message}")
        mock_read_excel.reset_mock()


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_with_none_dataframe(mock_read_excel):
    """Тест, когда pd.read_excel возвращает None"""
    mock_read_excel.return_value = None
    file_path = "test.xlsx"

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_excel(file_path)

    mock_read_excel.assert_called_once_with(file_path)
    assert result == []
    mock_print.assert_called_once()


@patch("read_csv_excel.pd.read_excel")
def test_transactions_from_excel_empty_string_file_path(mock_read_excel):
    """Тест с пустым путем к файлу для Excel"""
    mock_read_excel.side_effect = FileNotFoundError()
    file_path = ""

    with patch("builtins.print") as mock_print:
        result = load_transactions_from_excel(file_path)

    mock_read_excel.assert_called_once_with(file_path)
    assert result == []
    mock_print.assert_called_once_with("Ошибка: Файл  не найден")


# Тесты для нормализации ключей с разными форматами
@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_with_mixed_case_keys(mock_read_csv):
    """Тест нормализации ключей с разным регистром"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [
            {"ID": 1, "AMOUNT": 100, "CURRENCY_NAME": "RUB"},
            {"ID": 2, "AMOUNT": 200, "CURRENCY_NAME": "USD"}
        ]
        mock_read_csv.return_value = mock_df
        file_path = "test.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        assert result == [
            {"id": 1, "amount": 100, "currency_name": "RUB"},
            {"id": 2, "amount": 200, "currency_name": "USD"}
        ]
        mock_print.assert_called_once_with("Успешно загружено 2 транзакций из CSV")


@patch("read_csv_excel.pd.read_csv")
def test_load_transactions_from_csv_with_whitespace_in_keys(mock_read_csv):
    """Тест нормализации ключей с пробелами"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [
            {"  id  ": 1, "  amount  ": 100, "  currency_name  ": "RUB"}
        ]
        mock_read_csv.return_value = mock_df
        file_path = "test.csv"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_csv(file_path)

        assert result == [
            {"id": 1, "amount": 100, "currency_name": "RUB"}
        ]
        mock_print.assert_called_once_with("Успешно загружено 1 транзакций из CSV")


@patch("read_csv_excel.pd.read_excel")
def test_load_transactions_from_excel_with_mixed_case_keys(mock_read_excel):
    """Тест нормализации ключей с разным регистром для Excel"""
    with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [
            {"ID": 1, "AMOUNT": 150, "CURRENCY_NAME": "EUR"}
        ]
        mock_read_excel.return_value = mock_df
        file_path = "test.xlsx"

        with patch("builtins.print") as mock_print:
            result = load_transactions_from_excel(file_path)

        assert result == [
            {"id": 1, "amount": 150, "currency_name": "EUR"}
        ]
        mock_print.assert_called_once_with("Успешно загружено 1 транзакций из Excel")


# Тест для проверки импорта
def test_module_import():
    """Тест проверяющий корректный импорт"""
    assert callable(load_transactions_from_csv)
    assert callable(load_transactions_from_excel)


def test_path_correct():
    """Тест корректности расчета путей"""
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    expected_excel_path = os.path.join(project_root, "data", "transactions_excel.xlsx")
    expected_csv_path = os.path.join(project_root, "data", "transactions.csv")

    assert "tests" in current_dir
    assert "data" in expected_excel_path
    assert "data" in expected_csv_path
    assert "transactions_excel.xlsx" in expected_excel_path
    assert "transactions.csv" in expected_csv_path


def test_function_docstring():
    """Тест наличия и содержания docstrings"""
    assert load_transactions_from_csv.__doc__ is not None
    assert "Загружает список" in load_transactions_from_csv.__doc__
    assert "csv" in load_transactions_from_csv.__doc__.lower()

    assert load_transactions_from_excel.__doc__ is not None
    assert "Excel" in load_transactions_from_excel.__doc__


def test_return_type_is_list():
    """Тест, проверяющий, что функции возвращают список"""
    with patch("read_csv_excel.pd.read_csv") as mock_read_csv:
        with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
            mock_df = MockDataFrame.return_value
            mock_df.to_dict.return_value = [{"id": 1}]
            mock_read_csv.return_value = mock_df
            result = load_transactions_from_csv("test.csv")
            assert isinstance(result, list)

    with patch("read_csv_excel.pd.read_excel") as mock_read_excel:
        with patch("read_csv_excel.pd.DataFrame") as MockDataFrame:
            mock_df = MockDataFrame.return_value
            mock_df.to_dict.return_value = [{"id": 1}]
            mock_read_excel.return_value = mock_df
            result = load_transactions_from_excel("test.xlsx")
            assert isinstance(result, list)


# Интеграционный тест с реальными файлами (опционально)
def test_integration_with_real_files():
    """Интеграционный тест с реальными файлами (пропускается, если файлов нет)"""
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)

    excel_path = os.path.join(project_root, "data", "transactions_excel.xlsx")
    csv_path = os.path.join(project_root, "data", "transactions.csv")

    if not os.path.exists(excel_path) or not os.path.exists(csv_path):
        pytest.skip("Реальные файлы не найдены, пропускаем интеграционный тест")

    try:
        excel_result = load_transactions_from_excel(excel_path)
        csv_result = load_transactions_from_csv(csv_path)

        assert isinstance(excel_result, list)
        assert isinstance(csv_result, list)

        if excel_result:
            assert isinstance(excel_result[0], dict)
        if csv_result:
            assert isinstance(csv_result[0], dict)

    except Exception as e:
        pytest.fail(f"Интеграционный тест упал с ошибкой: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])