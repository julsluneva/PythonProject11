# 💼 Smart Bank Transaction Processor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green.svg)
![Testing](https://img.shields.io/badge/Testing-132%20Tests%20✓-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-90%25%20✓-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Умная система для обработки банковских транзакций с поддержкой множества форматов и валютных операций в реальном времени**

[Особенности](#-особенности) • [Быстрый старт](#-быстрый-старт) • [Использование](#-использование) • [Тестирование](#-тестирование)

</div>

## 🌟 О проекте

Smart Bank Transaction Processor — это мощный Python-фramework для работы с банковскими транзакциями. Система предоставляет полный цикл обработки финансовых данных: от чтения различных форматов файлов до безопасного отображения и конвертации валют.

### 🎯 Ключевые возможности

| Модуль | Функциональность | Статус |
|--------|------------------|---------|
| **📊 Чтение данных** | JSON, CSV, Excel файлы | ✅ Готов |
| **🔐 Безопасность** | Маскирование карт и счетов | ✅ Готов |
| **💱 Конвертация** | Реальные курсы валют через API | ✅ Готов |
| **🔄 Генерация** | Тестовые данные и номера карт | ✅ Готов |
| **⚙️ Обработка** | Фильтрация и сортировка | ✅ Готов |
| **📝 Логирование** | Детальный аудит операций | ✅ Готов |

## 🚀 Быстрый старт

### 1. Клонирование и настройка
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd bank-transaction-processor

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```
### 2. Настройка API (опционально)
```bash
# Создайте файл .env для API ключа
echo "API_KEY=your_exchangerate_api_key_here" > .env
```
### 3. Проверка установки
```bash
from src.read_csv_excel import load_transactions_from_csv, load_transactions_from_excel

# Тестовая загрузка данных

csv_data = load_transactions_from_csv("data/transactions.csv")
excel_data = load_transactions_from_excel("data/transactions_excel.xlsx")

print(f"✅ Успешно загружено {len(csv_data)} CSV и {len(excel_data)} Excel транзакций")
```
## 💡Примеры использования
### 🔒 Безопасное маскирование данных
```bash
from src.masks import get_mask_card_number, get_mask_account

# Маскирование номера карты
card_mask = get_mask_card_number("1234567812345678")
print(f"Карта: {card_mask}")  # "1234 56** **** 5678"

# Маскирование номера счета  
account_mask = get_mask_account("12345678901234567890")
print(f"Счет: {account_mask}")  # "**7890"

# Универсальное маскирование через виджет
from src.widget import mask_account_card
print(mask_account_card("Visa Platinum 1234567812345678"))  # "Visa Platinum 56** **** 3456"
```
### 📈Обработка транзакций
```bash
from src.processing import filter_by_state, sort_by_date

# Фильтрация выполненных операций
executed_ops = filter_by_state(transactions, "EXECUTED")

# Сортировка по дате (новые сверху)
recent_ops = sort_by_date(executed_ops)

print(f"Найдено {len(recent_ops)} выполненных операций")
```
### 💱 Конвертация валют в реальном времени
```bash
from src.external_api import convert_currency

# Пример транзакции в USD
transaction = {
    "operationAmount": {
        "amount": "150.00", 
        "currency": {"code": "USD"}
    }
}

# Автоматическая конвертация в рубли
amount_rub = convert_currency(transaction)
print(f"💵 $150.00 = {amount_rub:.2f} ₽")  # "💵 $150.00 = 11250.00 ₽"
```
### 🔄Генерация тестовых данных
```bash
from src.generators import card_number_generator, filter_by_currency

# Генерация номеров карт
card_gen = card_number_generator(1, 9)
for i in range(3):
    print(f"Карта {i+1}: {next(card_gen)}")

# Фильтрация по валюте
usd_transactions = list(filter_by_currency(transactions, "USD"))
print(f"Найдено {len(usd_transactions)} транзакций в USD")
```
### 📅Форматирование дат
```bash
from src.widget import get_date

# Конвертация даты в удобный формат
iso_date = "2023-12-25T15:30:00"
formatted_date = get_date(iso_date)
print(f"📅 {formatted_date}")  # "📅 25.12.2023"
```
### 🧪Тестирование
#### Полный цикл тестирования
```bash
# Запуск всех тестов
pytest tests/ -v

# Проверка покрытия кода
coverage run -m pytest tests/
coverage html
coverage report

# Открыть детальный отчет в браузере
open htmlcov/index.html
```
#### Целевое тестирование
```bash
# Тесты безопасности
pytest tests/test_masks.py -v

# Тесты API и конвертации валют
pytest tests/test_external_api.py -v

# Тесты генераторов данных
pytest tests/test_generators.py -k "test_card"

# Тесты обработки файлов
pytest tests/test_read_csv_excel.py -v
```
#### Статус тестирования
```bash
✅ test_masks.py - 100% покрытие
✅ test_external_api.py - 95% покрытие  
✅ test_generators.py - 92% покрытие
✅ test_processing.py - 88% покрытие
✅ test_read_csv_excel.py - 85% покрытие
✅ Всего: 132 теста, 90%+ покрытие
```
### 🔧Расширенные возможности
#### Кэширование курсов валют
```bash
from src.external_api import get_exchange_rate

# Первый вызов - запрос к API
rate1 = get_exchange_rate("USD", "RUB")

# Повторный вызов - данные из кэша
rate2 = get_exchange_rate("USD", "RUB")

print(f"Курс из кэша: {rate2}")  # Мгновенный ответ
```
#### Детальное логирование
```bash
import logging
from src.masks import get_mask_card_number

# Автоматическое логирование в masks.log
try:
    masked = get_mask_card_number("1234567812345678")
    print(f"Результат: {masked}")
except ValueError as e:
    print(f"Ошибка: {e}")
# Подробности в logs/masks.log
```
#### Обработка ошибок
```bash
from src.read_csv_excel import load_transactions_from_csv

# Автоматическая обработка ошибок файлов
result = load_transactions_from_csv("nonexistent.csv")
if not result:
    print("Файл не найден, но программа продолжает работу")
```
### 📊 Мониторинг и логи
```bash
Система автоматически создает детальные логи:

logs/masks.log - операции маскирования

logs/utils.log - работа с утилитами

Автоматическое ротирование и очистка

# Пример просмотра логов
with open("logs/masks.log", "r") as log_file:
    recent_entries = log_file.readlines()[-10:]
    for entry in recent_entries:
        print(entry.strip())
```
### 🛡 Безопасность
```bash
✅ Валидация данных на всех уровнях

✅ Маскирование конфиденциальной информации

✅ Безопасное хранение API ключей

✅ Логирование подозрительных операций

✅ Обработка исключений без утечек данных
```
### Требования к коду
```bash
✅ Наличие тестов для новой функциональности

✅ Покрытие кода не менее 85%

✅ Соответствие PEP8

✅ Обновление документации
```
### 📄Лицензия
```bash
Этот проект распространяется под лицензией MIT.
```
