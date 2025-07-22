import pytest

from src.processing import filter_by_state, sort_by_date

bank_oper = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.fixture
def sample_data():
    return bank_oper.copy()


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("", []),
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    """Тестирование фильтрации операций по состоянию"""
    filtered = filter_by_state(sample_data, state)
    assert [х["id"] for х in filtered] == expected_ids


def test_filter_by_state_default(sample_data):
    """Тестирование фильтрации операций со значением по умолчанию"""
    filtered = filter_by_state(sample_data)
    assert [х["id"] for х in filtered] == [41428829, 939719570]


# Тесты для sort_by_date
# тестирования сортировки
@pytest.mark.parametrize("reverse, expected_first_date", [(True, 41428829), (False, 939719570)])
def test_sort_by_date(sample_data, reverse, expected_first_date):
    sorted_operations = sort_by_date(sample_data, reverse=reverse)
    assert sorted_operations[0]["id"] == expected_first_date


@pytest.mark.parametrize(
    "operations, reverse",
    [
        ([{"id": 1, "date": "2023-02-30T00:00:00"}], True),  # Некорректная дата (30 февраля)
        ([{"id": 2, "date": "not-a-date"}], False),  # Не дата, а строка
        ([], True),  # Пустой список
    ],
)
def test_sort_by_date_invalid(operations, reverse):
    """Тест обработки некорректных дат или пустого списка."""
    # Проверяем, что функция не падает и возвращает список (без проверки порядка)
    result = sort_by_date(operations, reverse=reverse)
    assert isinstance(result, list)
