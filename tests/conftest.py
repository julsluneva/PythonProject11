import pytest


@pytest.fixture(autouse=True)
def clear_cache():
    """Фикстура для очистки кэша перед каждым тестом"""
    from src.external_api import cached_rates

    cached_rates.clear()
    yield
    cached_rates.clear()
