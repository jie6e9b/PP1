import pytest


@pytest.fixture
def valid_card_number() -> str:
    """Фикстура для валидного номера карты в виде строки."""
    return "1234567890123456"


@pytest.fixture
def valid_card_number_int() -> int:
    """Фикстура для валидного номера карты в виде целого числа."""
    return 1234567890123456


@pytest.fixture
def transaction_data():
    """Фикстура, возвращающая тестовые данные транзакций"""
    return [{
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }, {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }, {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "RUB",
                "code": "RUB"
            }
        },
        "description": "Рублевый перевод",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }]
