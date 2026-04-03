```markdown
 API тестирование микросервиса объявлений Avito

 О проекте

Проект содержит автоматизированные тесты для API микросервиса объявлений Avito (https://qa-internship.avito.com).

 Что тестируется
- Создание объявлений (POST /api/1/item)
- Получение объявления по ID (GET /api/1/item/{id})
- Получение объявлений продавца (GET /api/1/{sellerId}/item)
- Получение статистики (GET /api/1/statistic/{id})

 Особенности реализации
- Тесты независимы и воспроизводимы
- Генерация уникальных sellerId в диапазоне 111111-999999
- Поддержка параллельного запуска тестов
- Интеграция с Allure для формирования отчётов
- Настроены линтеры (flake8) и форматтер (black)

---

 Результаты тестирования

ВАЖНО: Тесты падают НЕ из-за ошибок в автотестах, а из-за реального бага в API.

 Статистика выполнения
| Показатель | Значение |
|------------|----------|
| Всего тестов | 21 |
| Пройдено | 9 |
| Провалено | 9 |
| Пропущено | 3 |

 Распределение по категориям
| Категория | Пройдено | Провалено | Пропущено |
|-----------|----------|-----------|-----------|
| Негативные сценарии | 9 | 0 | 0 |
| Позитивные сценарии | 0 | 7 | 2 |
| Идемпотентность | 1 | 3 | 0 |
| E2E сценарии | 0 | 1 | 0 |
| Производительность | 1 | 0 | 1 |

 Найденный баг (критический)

**БАГ-001**: POST /api/1/item всегда возвращает 400 "поле likes обязательно"

Описание: При попытке создать объявление сервер возвращает ошибку валидации даже когда поле `likes` присутствует в запросе в любом формате.

Воспроизведение бага:
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H "Content-Type: application/json" \
  -d '{"sellerId": 123456, "name": "Test", "price": 100, "likes": 0}'

# Ответ:
# {"result":{"message":"поле likes обязательно","messages":{}},"status":"400"}
```

Ожидаемый результат: HTTP 200 OK с ID созданного объявления.

Полное описание багов см. в файле BUGS.md.

---

## Требования к окружению

- Python 3.9 или выше
- pip (менеджер пакетов Python)
- Allure (опционально, для формирования отчётов)

---

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd avito-api-tests
```

### 2. Создание виртуального окружения
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка Allure (опционально)

Для формирования красивых отчётов рекомендуется установить Allure.

```bash
# MacOS
brew install allure

# Linux (Ubuntu/Debian)
sudo apt-add-repository ppa:qameta/allure
sudo apt update
sudo apt install allure

# Windows
# Скачать с https://github.com/allure-framework/allure2/releases
# Добавить в PATH
```

---

## Запуск тестов

### Запуск всех тестов
```bash
pytest api_tests/ -v
```

### Запуск по маркерам
```bash
pytest -m smoke          # Быстрая проверка критического функционала
pytest -m regression     # Полная регрессия
pytest -m idempotency    # Тесты идемпотентности
pytest -m corner         # Граничные случаи
pytest -m performance    # Тесты производительности
```

### Запуск конкретного файла
```bash
pytest api_tests/test_positive.py -v
pytest api_tests/test_negative.py -v
pytest api_tests/test_idempotency.py -v
```

### Запуск с подробным выводом ошибок
```bash
pytest api_tests/ -v --tb=long
```

### Параллельный запуск
```bash
pytest -n auto api_tests/
```

---

## Формирование Allure отчёта

### 1. Запуск тестов с сохранением результатов
```bash
pytest api_tests/ --alluredir=allure-results
```

### 2. Генерация отчёта
```bash
allure generate allure-results -o allure-report --clean
```

### 3. Открытие отчёта в браузере
```bash
allure open allure-report
```

Отчёт содержит:
- Общую статистику выполнения
- Графики прохождения тестов
- Подробные шаги каждого теста
- Вложения (логи, результаты запросов)
- Время выполнения тестов

---

## Линтеры и форматтеры

### Проверка стиля кода
```bash
flake8 api_tests/
```

### Автоматическое форматирование
```bash
black api_tests/
```

### Настройки линтеров
- Максимальная длина строки: 120 символов
- Игнорируемые правила: E203, W503
- Конфигурация в файлах `.flake8` и `pyproject.toml`

---

## Структура проекта

```
avito-api-tests/
├── api_tests/                      # Основная директория с тестами
│   ├── __init__.py
│   ├── conftest.py                 # Pytest фикстуры
│   ├── test_positive.py            # Позитивные тесты
│   ├── test_negative.py            # Негативные тесты
│   ├── test_idempotency.py         # Тесты идемпотентности
│   ├── test_e2e.py                 # E2E сценарии
│   ├── test_performance.py         # Тесты производительности
│   └── utils/
│       ├── __init__.py
│       ├── api_client.py           # API клиент
│       ├── data_generator.py       # Генерация тестовых данных
│       └── assertions.py           # Кастомные ассерты
├── TESTCASES.md                    # Описание тест-кейсов
├── BUGS.md                         # Баг-репорты
├── TEST_REPORT.md                  # Отчёт о тестировании
├── README.md                       # Документация
├── requirements.txt                # Зависимости
├── pytest.ini                      # Настройки pytest
├── .flake8                         # Настройки flake8
└── allure-results/                 # Результаты Allure (создаётся при запуске)
```

---

## Описание тестов

### Позитивные тесты (test_positive.py)
- Создание объявления с валидными данными
- Получение объявления по ID
- Получение всех объявлений продавца
- Получение статистики
- Создание с русскими символами

### Негативные тесты (test_negative.py)
- Создание без обязательных полей
- Пустое имя, отрицательная цена
- Price в виде строки
- Несуществующий ID
- Невалидный sellerId

### Идемпотентность (test_idempotency.py)
- Повторное создание одинаковых объявлений
- Многократные GET запросы
- Параллельное создание
- Лишние поля в JSON

### E2E сценарии (test_e2e.py)
- Полный жизненный цикл объявления
- Сквозная проверка всех эндпоинтов

### Производительность (test_performance.py)
- Время ответа API
- Создание 10 объявлений последовательно

---

## Переменные окружения

Проект не требует дополнительных переменных окружения. Все настройки находятся в конфигурационных файлах.

---

## CI/CD интеграция

Пример настройки для GitHub Actions:

```yaml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest api_tests/ -m smoke --alluredir=allure-results
      - uses: actions/upload-artifact@v3
        with:
          name: allure-results
          path: allure-results
```

---

## Устранение неполадок

### Ошибка импорта модулей
```bash
export PYTHONPATH=${PYTHONPATH}:$(pwd)
```

### Ошибка подключения к API
- Проверьте интернет-соединение
- Убедитесь, что сервер https://qa-internship.avito.com доступен

### Allure не найден
```bash
# Установка через npm (альтернативный способ)
npm install -g allure-commandline
```

### Тесты падают с ошибкой "поле likes обязательно"
Это ожидаемое поведение. См. BUGS.md для деталей. Тесты падают из-за реального бага в API.

---

## Документация

- [Тест-кейсы](TESTCASES.md) - полное описание тестов
- [Баг-репорты](BUGS.md) - найденные дефекты
- [Отчёт о тестировании](TEST_REPORT.md) - итоговые результаты

---

## Лицензия

Учебный проект для стажировки. Не для коммерческого использования.
```