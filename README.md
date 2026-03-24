# 💼 Smart Bank Transaction Processor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green.svg)
![Testing](https://img.shields.io/badge/Testing-239%20Tests%20✓-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-93%25%20✓-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Умная система для обработки банковских транзакций с поддержкой множества форматов и валютных операций в реальном времени**

[Особенности](#-особенности) • [Быстрый старт](#-быстрый-старт) • [Использование](#-использование) • [Тестирование](#-тестирование)

</div>

## 🌟 О проекте

Smart Bank Transaction Processor — это мощный Python-фramework для работы с банковскими транзакциями. 
Система предоставляет полный цикл обработки финансовых данных: от чтения различных форматов файлов до безопасного 
отображения и конвертации валют.

### 🎯 Ключевые возможности

| Модуль | Функциональность | Статус |
|--------|------------------|---------|
| **📊 Чтение данных** | JSON, CSV, Excel файлы | ✅ Готов |
| **🔐 Безопасность** | Маскирование карт и счетов | ✅ Готов |
| **💱 Конвертация** | Реальные курсы валют через API | ✅ Готов |
| **🔄 Генерация** | Тестовые данные и номера карт | ✅ Готов |
| **⚙️ Обработка** | Фильтрация, сортировка, поиск | ✅ Готов |
| **📊 Аналитика** | Подсчет операций по категориям | ✅ Готов |
| **🔍 Поиск** | Регулярные выражения в описаниях | ✅ Готов |
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
### 3. Запуск интерактивной программы
```bash
# Запуск основного приложения
python main.py
```
## 💡Примеры использования

### ⭐ Интерактивный режим работы
```bash
#Запустите main.py для интерактивной работы с программой
python main.py
# Программа предложит:
# 1. Выбрать источник данных (JSON/CSV/Excel)
# 2. Отфильтровать по статусу (EXECUTED/CANCELED/PENDING)
# 3. Отсортировать по дате
# 4. Выбрать только рублевые транзакции
# 5. Выполнить поиск по описанию
### 🔒 Безопасное маскирование данных
```
### 🔍 Поиск транзакций с регулярными выражениями
```bash
from src.processing import process_bank_search

# Поиск транзакций по описанию с использованием regex
transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Открытие вклада"},
    {"id": 3, "description": "Перевод с карты на карту"},
]

# Поиск без учета регистра
result = process_bank_search(transactions, "перевод")
print(f"Найдено {len(result)} транзакций")  # Найдено 2 транзакций

# Поиск со специальными символами (автоматическое экранирование)
result = process_bank_search(transactions, "Перевод (организации)")
```
### 📊 Статистика по категориям операций
```bash

from src.processing import process_bank_operations

transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Открытие вклада"},
    {"id": 3, "description": "Перевод с карты на карту"},
]

categories = ["Перевод", "Открытие", "Вклад"]
stats = process_bank_operations(transactions, categories)

print("Статистика по категориям:")
for category, count in stats.items():
    print(f"  {category}: {count} операций")
# Вывод:
#   Перевод: 2 операций
#   Открытие: 1 операций
#   Вклад: 1 операций
```
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
from src.processing import filter_by_state, sort_by_date, filter_by_currency

# Фильтрация выполненных операций
executed_ops = filter_by_state(transactions, "EXECUTED")

# Сортировка по дате (новые сверху)
recent_ops = sort_by_date(executed_ops)

# Фильтрация только рублевых транзакций
rub_ops = filter_by_currency(executed_ops, rub_only=True)

print(f"Найдено {len(rub_ops)} рублевых операций")
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
from src.display import format_date

# Конвертация даты в удобный формат
iso_date = "2023-12-25T15:30:00"
formatted_date = get_date(iso_date)
print(f"📅 {formatted_date}")  # "📅 25.12.2023"

# Альтернативный формат из модуля display
display_date = format_date(iso_date) # '25.12.2023'
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

# Тесты поиска с регулярными выражениями
pytest tests/test_processing.py -k "test_process_bank_search"
```
#### Статус тестирования
```bash
✅ test_main.py - 86% покрытие
✅ test_masks.py - 95% покрытие
✅ test_external_api.py - 96% покрытие  
✅ test_generators.py - 94% покрытие
✅ test_processing.py - 86% покрытие
✅ test_read_csv_excel.py - 100% покрытие
✅ test_utils.py - 100% покрытие
✅ test_widget.py - 85% покрытие
✅ Всего: 239 тестов, 93% покрытие
```
```bash
### 🔧Расширенные возможности
```
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

✅ Экранирование специальных символов в поиске

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
