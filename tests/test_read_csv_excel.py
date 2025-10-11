import pytest
from unittest.mock import patch
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from read_csv_excel import(
load_transactions_from_csv,
load_transactions_from_excel
)

@patch('read_csv_excel.pd.read_csv')
def test_load_transactions_from_csv_success(mock_read_csv):
    """Тест успешной загрузки транзакций из CSV"""

    with patch('read_csv_excel.pd.DataFrame') as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200}
        ]
        mock_read_csv.return_value = mock_df
        file_path = 'test.csv'

        with patch('read_csv_excel.print') as mock_print:
            #вызываем тестируемую функцию с тестовым путем
            result = load_transactions_from_csv(file_path)
        # Проверяем, что pd.read_csv был вызван 1 раз с правильным путем
        mock_read_csv.assert_called_once_with(file_path)
        # Проверяем, что метор to_dict был вызван один раз с параметром 'records'
        mock_df.to_dict.assert_called_once_with('records')
        # Проверяем, что функция вернула ожидаемые данные
        assert result == [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200}
        ]
        # Проверяем, что print вызвана с правильным сообщением
        mock_print.assert_called_once_with(" Успешно загружено 2 транзакций из CSV")


# Тест для проверки ошибки 'файл не найден'
@patch('read_csv_excel.pd.read_csv')
def test_load_transactions_from_csv_file_not_found(mock_read_csv):
    """Тест обработки ошибки FileNotFoundError для CSV"""

    # делаем заглушку, чтобы выбрасывала исключение
    mock_read_csv.side_effect = FileNotFoundError('File not found')

    file_path = 'nonexistent.csv'
    with patch('read_csv_excel.print') as mock_print:
        result = load_transactions_from_csv(file_path)
        # Проверяем, что read_csv был вызван с правильным путем
        mock_read_csv.assert_called_once_with(file_path)
        # Проверяем, что при ошибке функция возвращает пустой список
        assert result == []
        # Проверяем, что выведено сообщение об ошибке
        mock_print.assert_called_once_with('Ошибка: Файл nonexistent.csv не найден')

@patch('read_csv_excel.pd.read_csv')
def test_load_transactions_from_csv_general_error(mock_read_csv):
    """Тест для обработки общей ошибки для CSV"""

    mock_read_csv.side_effect = Exception('Some error')
    file_path = 'corrupted.csv'

    with patch('read_csv_excel.print') as mock_print:
        result = load_transactions_from_csv(file_path)

    mock_read_csv.assert_called_once_with(file_path)
    assert result == []
    mock_print.assert_called_once_with('Ошибка при чтении CSV файла: Some error')

# Тест для успешной загрузки Excel
@patch('read_csv_excel.pd.read_excel')
def test_load_transactions_from_excel_success(mock_read_excel):
    """Тест успешной загрузки транзакций из Excel"""

    with patch('read_csv_excel.pd.DataFrame') as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [
            {'id': 1, 'amount': 150},
            {'id': 2, 'amount': 250},
            {'id': 3, 'amount': 350}
        ]
        mock_read_excel.return_value = mock_df
        file_path = 'test.xlsx'

    with patch('read_csv_excel.print') as mock_print:
        result = load_transactions_from_excel(file_path)

    mock_read_excel.assert_called_once_with(file_path)
    mock_df.to_dict.assert_called_once_with('records')
    assert result == [
        {'id': 1, 'amount': 150},
        {'id': 2, 'amount': 250},
        {'id': 3, 'amount': 350}
    ]
    mock_print.assert_called_once_with('Успешно загружено 3 транзакций из Excel')

@patch('read_csv_excel.pd.read_excel')
def test_load_transactions_from_excel_file_not_found(mock_read_excel):
    """Тест для обработки ошибки FileNotFoundError для Excel"""

    mock_read_excel.side_effect = FileNotFoundError('Excel file not found')
    file_path = 'nonexistent.xlsx'

    with patch('read_csv_excel.print') as mock_print:
        result = load_transactions_from_excel(file_path)

    mock_read_excel.assert_called_once_with(file_path)
    assert result == []
    mock_print.assert_called_once_with('Ошибка: Файл nonexistent.xlsx не найден')

@patch('read_csv_excel.pd.read_csv')
def test_load_transactions_from_csv_empty_file(mock_read_csv):
    """Тест загрузки пустого CSV файла"""

    with patch('read_csv_excel.pd.DataFrame') as MockDataFrame:
        mock_df = MockDataFrame.return_value
        mock_df.to_dict.return_value = [] # Пустой список
        mock_read_csv.return_value = mock_df
        file_path = 'empty.csv'

    with patch('read_csv_excel.print') as mock_print:
        result = load_transactions_from_csv(file_path)

    mock_read_csv.assert_called_once_with(file_path)
    mock_df.to_dict.assert_called_once_with('records')
    assert result == [] # Должен вернуть пустой список
    mock_print.assert_called_once_with(' Успешно загружено 0 транзакций из CSV')

def test_path_correct():
    """Тест корректности расчета путей"""

    current_dir = os.path.dirname(__file__)
    print(f"Текущая директория: {current_dir}")

    project_root = os.path.dirname(current_dir)
    print(f"Корень проекта: {project_root}")

    expected_excel_path = os.path.join(project_root, 'data', 'transactions_excel.xlsx')
    expected_csv_path = os.path.join(project_root, 'data', 'transactions.csv')

    assert 'tests' in current_dir, "Текущая директория должна содержать 'tests'"
    assert 'data' in expected_excel_path, "Путь к Excel должен содержать 'data'"
    assert 'data' in expected_csv_path, "Путь к CSV должен содержать 'data'"
    assert 'transactions_excel.xlsx' in expected_excel_path
    assert 'transactions.csv' in expected_csv_path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])