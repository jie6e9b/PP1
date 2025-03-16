import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_filter_by_usd(transaction_data):
    """Проверяет фильтрацию транзакций по валюте USD"""
    usd_transactions = list(filter_by_currency(transaction_data, "USD"))
    assert len(usd_transactions) == 2
    for transaction in usd_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_rub(transaction_data):
    """Проверяет фильтрацию транзакций по валюте RUB"""
    rub_transactions = list(filter_by_currency(transaction_data, "RUB"))
    assert len(rub_transactions) == 1
    for transaction in rub_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_eur(transaction_data):
    """Проверяет фильтрацию транзакций по валюте которой нет в списке
    + проверяем, что функция возвращает пустой список, а не завершается ошибкой"""
    eur_transactions = list(filter_by_currency(transaction_data, "EUR"))
    assert len(eur_transactions) == 0
    assert eur_transactions == []


def test_filter_with_empty_list():
    """Проверяет работу функции с пустым списком транзакций"""
    empty_list = []
    result = list(filter_by_currency(empty_list, "USD"))
    # Проверяем, что функция корректно обрабатывает пустой список
    assert result == []


def test_transaction_descriptions_basic(transaction_data):
    """Проверяет базовую функциональность генератора описаний транзакций"""
    descriptions = list(transaction_descriptions(transaction_data))

    # Проверяем, что количество описаний соответствует количеству транзакций
    assert len(descriptions) == 3

    # Проверяем содержимое описаний
    assert descriptions[0] == "Перевод организации"
    assert descriptions[1] == "Перевод со счета на счет"
    assert descriptions[2] == "Рублевый перевод"


def test_transaction_descriptions_empty_list():
    """Проверяет работу функции с пустым списком транзакций"""
    descriptions = list(transaction_descriptions([]))

    # Проверяем, что результат - пустой список
    assert descriptions == []


def test_transaction_descriptions_generator(transaction_data):
    """Проверяет, что функция действительно является генератором"""
    result = transaction_descriptions(transaction_data)

    # Проверяем, что результат - итерируемый объект, но не список
    assert hasattr(result, '__iter__')
    assert not isinstance(result, list)

    # Проверяем, что можно получить значения по одному
    assert next(result) == "Перевод организации"
    assert next(result) == "Перевод со счета на счет"
    assert next(result) == "Рублевый перевод"

    # Проверяем, что генератор исчерпан
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize("start, count, expected", [
    (1, 5, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003",
            "0000 0000 0000 0004", "0000 0000 0000 0005"]),
    (42, 1, ["0000 0000 0000 0042"]),
    (9000, 3, ["0000 0000 0000 9000", "0000 0000 0000 9001", "0000 0000 0000 9002"])
])
def test_card_number_generator_basic(start, count, expected):
    """Проверяет базовую функциональность генератора номеров карт"""
    cards = list(card_number_generator(start, start + count - 1))
    # Проверяем количество сгенерированных карт
    assert len(cards) == count
    # Проверяем правильность форматирования и значений
    assert cards == expected


@pytest.mark.parametrize("number, expected_format", [
    (1234567890123456, "1234 5678 9012 3456"),
    (1000, "0000 0000 0000 1000"),
    (1, "0000 0000 0000 0001"),
    (9999999999999999, "9999 9999 9999 9999")
])
def test_card_number_generator_format(number, expected_format):
    """Проверяет правильность форматирования номеров карт"""
    cards = list(card_number_generator(number, number))
    assert len(cards) == 1
    assert cards[0] == expected_format


@pytest.mark.parametrize("start, end, check_indices", [
    (9000, 9999, [(0, "0000 0000 0000 9000"), (999, "0000 0000 0000 9999"), (500, "0000 0000 0000 9500")]),
    (1, 100, [(0, "0000 0000 0000 0001"), (99, "0000 0000 0000 0100"), (50, "0000 0000 0000 0051")])
    ])
def test_card_number_generator_large_range(start, end, check_indices):
    """Проверяет генерацию карт в большом диапазоне"""
    cards = list(card_number_generator(start, end))
    assert len(cards) == end - start + 1
    # Проверяем карты на определенных позициях
    for idx, expected in check_indices:
        assert cards[idx] == expected


@pytest.mark.parametrize("start, end, error_msg", [
    (0, 10, "Начальное значение не находится в допустимом диапазоне"),
    (10000000000000000, 10000000000000001, "Начальное значение не находится в допустимом диапазоне"),
    (100, 99, "Конечное значение не находится в допустимом диапазоне"),
    (100, 10000000000000000, "Конечное значение не находится в допустимом диапазоне")
])
def test_card_number_generator_invalid_input(start, end, error_msg):
    """Проверяет обработку некорректных входных данных"""
    with pytest.raises(ValueError, match=error_msg):
        list(card_number_generator(start, end))
