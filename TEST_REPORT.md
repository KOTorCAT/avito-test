# Отчёт о тестировании API Avito

## Общая информация
- **Дата**: 2026-04-03
- **Тестировщик**: Кандидат на стажировку
- **Окружение**: https://qa-internship.avito.com
- **Всего тестов**: 21
- **Пройдено**: 9
- **Провалено**: 9
- **Пропущено**: 3

## Результаты по категориям

### Негативные тесты ✅ (100% проходимости)
- test_create_ad_missing_name ✅
- test_create_ad_empty_name ✅
- test_create_ad_negative_price ✅
- test_create_ad_string_price ✅
- test_get_ad_invalid_id ✅
- test_get_ads_invalid_seller ✅
- test_create_ad_null_price ✅

**Вывод**: Валидация API работает корректно.

### Позитивные тесты ❌ (0% проходимости)
Все позитивные тесты падают с ошибкой: