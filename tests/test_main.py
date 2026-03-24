"""Тесты для основного модуля main.py"""

import os
from unittest.mock import patch

# Импортируем функции для тестирования
from main import get_file_path, get_status_from_user, get_user_choice, read_json_file


class TestGetFilePath:
    """Тесты для функции get_file_path"""

    def test_get_file_path_correct(self):
        """Тест корректного формирования пути к файлу"""
        with patch("main.os.path.dirname") as mock_dirname:
            mock_dirname.return_value = "/test/project"

            result = get_file_path("test_file.txt")

            expected = os.path.join("/test/project", "data", "test_file.txt")
            assert os.path.normpath(result) == os.path.normpath(expected)

    def test_get_file_path_with_subdirectory(self):
        """Тест пути с поддиректорией"""
        with patch("main.os.path.dirname") as mock_dirname:
            mock_dirname.return_value = "/test/project"

            result = get_file_path("subdir/file.txt")

            expected = os.path.join("/test/project", "data", "subdir", "file.txt")
            assert os.path.normpath(result) == os.path.normpath(expected)


class TestReadJsonFile:
    """Тесты для функции read_json_file"""

    @patch("main.get_file_path")
    @patch("builtins.open")
    @patch("json.load")
    def test_read_json_file_success(self, mock_json_load, mock_open, mock_get_path):
        """Тест успешного чтения JSON файла"""
        mock_get_path.return_value = "/test/path/operations.json"
        mock_json_load.return_value = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]

        with patch("builtins.print") as mock_print:
            result = read_json_file()

            assert len(result) == 2
            mock_print.assert_called_with("Успешно загружено 2 транзакций из JSON")

    @patch("main.get_file_path")
    @patch("builtins.open")
    def test_read_json_file_file_not_found(self, mock_open, mock_get_path):
        """Тест обработки FileNotFoundError"""
        mock_get_path.return_value = "/test/path/operations.json"
        mock_open.side_effect = FileNotFoundError()

        with patch("builtins.print") as mock_print:
            result = read_json_file()

            assert result == []
            mock_print.assert_called_with("Файл не найден: /test/path/operations.json")

    @patch("main.get_file_path")
    @patch("builtins.open")
    @patch("json.load")
    def test_read_json_file_not_list(self, mock_json_load, mock_open, mock_get_path):
        """Тест когда JSON не является списком"""
        mock_get_path.return_value = "/test/path/operations.json"
        mock_json_load.return_value = {"id": 1, "state": "EXECUTED"}  # Это словарь, а не список

        with patch("builtins.print") as mock_print:
            result = read_json_file()

            assert result == []
            mock_print.assert_called_with("Ошибка: JSON файл должен содержать список")

    @patch("main.get_file_path")
    @patch("builtins.open")
    @patch("json.load")
    def test_read_json_file_json_decode_error(self, mock_json_load, mock_open, mock_get_path):
        """Тест обработки ошибки декодирования JSON"""
        mock_get_path.return_value = "/test/path/operations.json"
        import json

        error_message = "Expecting value: line 1 column 1 (char 0)"
        mock_json_load.side_effect = json.JSONDecodeError(error_message, "doc", 0)

        with patch("builtins.print") as mock_print:
            result = read_json_file()

            assert result == []
            # Проверяем, что сообщение начинается с нужного текста
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            assert call_args.startswith("Ошибка декодирования JSON")

    @patch("main.get_file_path")
    @patch("builtins.open")
    @patch("json.load")
    def test_read_json_file_general_exception(self, mock_json_load, mock_open, mock_get_path):
        """Тест обработки общего исключения"""
        mock_get_path.return_value = "/test/path/operations.json"
        mock_json_load.side_effect = Exception("Some error")

        with patch("builtins.print") as mock_print:
            result = read_json_file()

            assert result == []
            mock_print.assert_called_with("Ошибка при чтении JSON файла: Some error")


class TestGetUserChoice:
    """Тесты для функции get_user_choice"""

    @patch("main.input")
    def test_get_user_choice_valid_input(self, mock_input):
        """Тест корректного ввода пользователя"""
        mock_input.side_effect = ["да", "нет", "ДА", "НЕТ"]
        valid_choices = ["да", "нет"]

        result = get_user_choice("Выберите: ", valid_choices)
        assert result == "да"

        result = get_user_choice("Выберите: ", valid_choices)
        assert result == "нет"

    @patch("main.input")
    @patch("main.print")
    def test_get_user_choice_invalid_then_valid(self, mock_print, mock_input):
        """Тест сначала некорректного, затем корректного ввода"""
        mock_input.side_effect = ["неверно", "может быть", "да"]
        valid_choices = ["да", "нет"]

        result = get_user_choice("Выберите: ", valid_choices)

        mock_print.assert_called()
        assert result == "да"
        assert mock_input.call_count == 3

    @patch("main.input")
    def test_get_user_choice_case_insensitive(self, mock_input):
        """Тест регистронезависимого сравнения"""
        mock_input.return_value = "ДА"
        valid_choices = ["да", "нет"]

        result = get_user_choice("Выберите: ", valid_choices)

        assert result == "да"

    @patch("main.input")
    def test_get_user_choice_with_spaces(self, mock_input):
        """Тест обработки пробелов во вводе"""
        mock_input.return_value = "  да  "
        valid_choices = ["да", "нет"]

        result = get_user_choice("Выберите: ", valid_choices)

        assert result == "да"


class TestGetStatusFromUser:
    """Тесты для функции get_status_from_user"""

    @patch("main.input")
    @patch("main.print")
    def test_get_status_from_user_valid(self, mock_print, mock_input):
        """Тест корректного ввода статуса"""
        mock_input.return_value = "EXECUTED"

        result = get_status_from_user()

        assert result == "EXECUTED"

    @patch("main.input")
    @patch("main.print")
    def test_get_status_from_user_invalid_then_valid(self, mock_print, mock_input):
        """Тест сначала некорректного, затем корректного ввода статуса"""
        mock_input.side_effect = ["INVALID", "CANCELED"]

        result = get_status_from_user()

        assert result == "CANCELED"
        # Проверяем, что было сообщение об ошибке
        error_calls = [call for call in mock_print.call_args_list if "недоступен" in str(call)]
        assert len(error_calls) == 1


class TestMainFunction:
    """Тесты для основной функции main()"""

    @patch("main.display_transactions")
    @patch("main.filter_by_currency")
    @patch("main.filter_by_state")
    @patch("main.process_bank_search")
    @patch("main.process_bank_operations")
    @patch("main.sort_by_date")
    @patch("main.load_transactions_from_excel")
    @patch("main.load_transactions_from_csv")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_full_flow_json(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_load_csv,
        mock_load_excel,
        mock_sort_date,
        mock_process_operations,
        mock_process_search,
        mock_filter_state,
        mock_filter_currency,
        mock_display,
        mock_transactions,
    ):
        """Тест полного потока с выбором JSON файла"""
        mock_input.side_effect = ["1"]  # Выбор JSON
        mock_get_status.return_value = "EXECUTED"
        mock_get_user_choice.side_effect = ["нет", "нет", "нет"]
        mock_read_json.return_value = mock_transactions
        mock_filter_state.return_value = [t for t in mock_transactions if t["state"] == "EXECUTED"]
        mock_filter_currency.return_value = mock_filter_state.return_value

        from main import main

        main()

        mock_read_json.assert_called_once()
        mock_filter_state.assert_called_once_with(mock_transactions, "EXECUTED")
        mock_display.assert_called_once()

    @patch("main.display_transactions")
    @patch("main.filter_by_currency")
    @patch("main.filter_by_state")
    @patch("main.process_bank_search")
    @patch("main.process_bank_operations")
    @patch("main.sort_by_date")
    @patch("main.load_transactions_from_excel")
    @patch("main.load_transactions_from_csv")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_csv_file(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_load_csv,
        mock_load_excel,
        mock_sort_date,
        mock_process_operations,
        mock_process_search,
        mock_filter_state,
        mock_filter_currency,
        mock_display,
        mock_csv_transactions,
    ):
        """Тест выбора CSV файла"""
        mock_input.side_effect = ["2"]  # Выбор CSV
        mock_get_status.return_value = "CANCELED"
        mock_get_user_choice.side_effect = ["нет", "нет", "нет"]
        mock_load_csv.return_value = mock_csv_transactions
        mock_filter_state.return_value = [t for t in mock_csv_transactions if t["state"] == "CANCELED"]

        from main import main

        main()

        mock_load_csv.assert_called_once()
        mock_filter_state.assert_called_once_with(mock_csv_transactions, "CANCELED")

    @patch("main.display_transactions")
    @patch("main.filter_by_currency")
    @patch("main.filter_by_state")
    @patch("main.process_bank_search")
    @patch("main.process_bank_operations")
    @patch("main.sort_by_date")
    @patch("main.load_transactions_from_excel")
    @patch("main.load_transactions_from_csv")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_excel_file(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_load_csv,
        mock_load_excel,
        mock_sort_date,
        mock_process_operations,
        mock_process_search,
        mock_filter_state,
        mock_filter_currency,
        mock_display,
        mock_transactions,
    ):
        """Тест выбора Excel файла"""
        mock_input.side_effect = ["3"]  # Выбор Excel
        mock_get_status.return_value = "PENDING"
        mock_get_user_choice.side_effect = ["нет", "нет", "нет"]
        mock_load_excel.return_value = mock_transactions
        mock_filter_state.return_value = [t for t in mock_transactions if t["state"] == "PENDING"]

        from main import main

        main()

        mock_load_excel.assert_called_once()
        mock_filter_state.assert_called_once_with(mock_transactions, "PENDING")

    @patch("main.input")
    def test_main_invalid_file_choice(self, mock_input):
        """Тест некорректного выбора файла"""
        mock_input.return_value = "4"

        from main import main

        with patch("main.print") as mock_print:
            main()
            mock_print.assert_any_call("Некорректный выбор. Программа завершена.")

    @patch("main.display_transactions")
    @patch("main.filter_by_state")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_with_sorting(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_filter_state,
        mock_display,
        mock_transactions,
    ):
        """Тест с включенной сортировкой"""
        mock_input.side_effect = ["1"]
        mock_get_status.return_value = "EXECUTED"
        mock_get_user_choice.side_effect = ["да", "убыванию", "нет", "нет"]
        mock_read_json.return_value = mock_transactions
        executed_transactions = [t for t in mock_transactions if t["state"] == "EXECUTED"]
        mock_filter_state.return_value = executed_transactions

        from main import main

        with patch("main.sort_by_date") as mock_sort:
            mock_sort.return_value = sorted(executed_transactions, key=lambda x: x["date"], reverse=True)
            main()

            # Проверяем вызов с позиционными аргументами
            mock_sort.assert_called_once_with(executed_transactions, True)

    @patch("main.display_transactions")
    @patch("main.filter_by_state")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_with_rub_only(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_filter_state,
        mock_display,
        mock_transactions,
    ):
        """Тест с фильтрацией только рублевых транзакций"""
        mock_input.side_effect = ["1"]
        mock_get_status.return_value = "EXECUTED"
        mock_get_user_choice.side_effect = ["нет", "да", "нет"]
        mock_read_json.return_value = mock_transactions
        executed_transactions = [t for t in mock_transactions if t["state"] == "EXECUTED"]
        mock_filter_state.return_value = executed_transactions

        from main import main

        with patch("main.filter_by_currency") as mock_filter_currency:
            rub_transactions = [t for t in executed_transactions if t["operationAmount"]["currency"]["code"] == "RUB"]
            mock_filter_currency.return_value = rub_transactions
            main()

            mock_filter_currency.assert_called_once_with(executed_transactions, rub_only=True)

    @patch("main.display_transactions")
    @patch("main.filter_by_state")
    @patch("main.read_json_file")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_main_with_search(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_read_json,
        mock_filter_state,
        mock_display,
        mock_transactions,
    ):
        """Тест с поиском по описанию"""
        mock_input.side_effect = ["1", "перевод"]
        mock_get_status.return_value = "EXECUTED"
        mock_get_user_choice.side_effect = ["нет", "нет", "да"]
        mock_read_json.return_value = mock_transactions
        executed_transactions = [t for t in mock_transactions if t["state"] == "EXECUTED"]
        mock_filter_state.return_value = executed_transactions

        from main import main

        with patch("main.process_bank_search") as mock_search:
            search_results = [t for t in executed_transactions if "перевод" in t["description"].lower()]
            mock_search.return_value = search_results
            main()

            mock_search.assert_called_once_with(executed_transactions, "перевод")

    @patch("main.input")
    def test_main_no_transactions_loaded(self, mock_input):
        """Тест когда не удалось загрузить транзакции"""
        mock_input.side_effect = ["1"]

        from main import main

        with patch("main.read_json_file") as mock_read_json:
            mock_read_json.return_value = []
            with patch("main.print") as mock_print:
                main()
                mock_print.assert_any_call("Не удалось загрузить транзакции или файл пуст.")

    @patch("main.input")
    def test_main_no_transactions_after_filter(self, mock_input):
        """Тест когда после фильтрации не осталось транзакций"""
        mock_input.side_effect = ["1"]

        from main import main

        with patch("main.read_json_file") as mock_read_json:
            mock_read_json.return_value = [{"id": 1, "state": "CANCELED"}]
            with patch("main.get_status_from_user") as mock_get_status:
                mock_get_status.return_value = "EXECUTED"
                with patch("main.filter_by_state") as mock_filter_state:
                    mock_filter_state.return_value = []
                    with patch("main.print") as mock_print:
                        main()
                        # Проверяем сообщение о пустом результате
                        found = any(
                            "Не найдено ни одной транзакции" in str(call) for call in mock_print.call_args_list
                        )
                        assert found


class TestIntegrationScenarios:
    """Интеграционные тесты"""

    @patch("main.display_transactions")
    @patch("main.process_bank_search")
    @patch("main.process_bank_operations")
    @patch("main.filter_by_currency")
    @patch("main.sort_by_date")
    @patch("main.filter_by_state")
    @patch("main.load_transactions_from_csv")
    @patch("main.get_status_from_user")
    @patch("main.get_user_choice")
    @patch("main.input")
    def test_complete_workflow(
        self,
        mock_input,
        mock_get_user_choice,
        mock_get_status,
        mock_load_csv,
        mock_filter_state,
        mock_sort_date,
        mock_filter_currency,
        mock_process_operations,
        mock_process_search,
        mock_display,
        mock_csv_transactions,
    ):
        """Полный рабочий процесс с всеми опциями"""
        mock_input.side_effect = ["2", "перевод"]
        mock_get_status.return_value = "EXECUTED"
        mock_get_user_choice.side_effect = ["да", "убыванию", "да", "да"]

        test_transactions = mock_csv_transactions

        mock_load_csv.return_value = test_transactions
        executed_transactions = [t for t in test_transactions if t["state"] == "EXECUTED"]
        mock_filter_state.return_value = executed_transactions
        mock_sort_date.return_value = sorted(executed_transactions, key=lambda x: x["date"], reverse=True)
        rub_transactions = [
            t for t in executed_transactions if t.get("currency_code") == "RUB" or t.get("currency_name") == "руб."
        ]
        mock_filter_currency.return_value = rub_transactions
        search_results = [t for t in rub_transactions if "перевод" in t["description"].lower()]
        mock_process_search.return_value = search_results

        from main import main

        main()

        mock_load_csv.assert_called_once()
        mock_filter_state.assert_called_once_with(test_transactions, "EXECUTED")
        # Проверяем вызов с позиционными аргументами
        mock_sort_date.assert_called_once_with(executed_transactions, True)
        mock_filter_currency.assert_called_once_with(mock_sort_date.return_value, rub_only=True)
        mock_process_search.assert_called_once_with(mock_filter_currency.return_value, "перевод")
        mock_display.assert_called_once_with(mock_process_search.return_value)
