from typing import List, Dict, Iterable

# transactions = [
#     {
#         "id": 939719570,
#         "state": "EXECUTED",
#         "date": "2018-06-30T02:08:58.425572",
#         "operationAmount": {
#             "amount": "9824.07",
#             "currency": {
#                 "name": "USD",
#                 "code": "USD"
#             }
#         },
#         "description": "Перевод организации",
#         "from": "Счет 75106830613657916952",
#         "to": "Счет 11776614605963066702"
#     },
#     {
#         "id": 142264268,
#         "state": "EXECUTED",
#         "date": "2019-04-04T23:20:05.206878",
#         "operationAmount": {
#             "amount": "79114.93",
#             "currency": {
#                 "name": "USD",
#                 "code": "USD"
#             }
#         },
#         "description": "Перевод со счета на счет",
#         "from": "Счет 19708645243227258542",
#         "to": "Счет 75651667383060284188"
#     }
# ]


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterable[Dict]:
    """ Фильтрует список транзакций по указанной валюте.
    Args: transactions: Список словарей, представляющих транзакции.
    currency: Строка с кодом валюты для фильтрации (например, "USD").
    Returns: Итератор, который последовательно выдает транзакции с указанной валютой.
    Example: >>> usd_transactions = filter_by_currency(transactions, "USD")  >>> transaction = next(usd_transactions)
    Note: Валюта находится во вложенной структуре:
    transaction["operationAmount"]["currency"]["code"] """

    return filter(lambda transaction: transaction["operationAmount"]["currency"]["code"] == currency, transactions)

# # Проверим работу фильтра
# usd_transactions = filter_by_currency(transactions, "USD")
# # Выводим результаты
# for i in range(2):
#     print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict]) -> Iterable[str]:
    """ Генератор, который возвращает описания транзакций по очереди.
    Args: transactions: список словарей с транзакциями
    Yields: строка с описанием каждой транзакции
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")

# # Проверим работу фильтра генератора
# descriptions = transaction_descriptions(transactions)
# # Выводим результаты
# for i in range(2):
#     print(next(descriptions))


def card_number_generator(start: int, end: int) -> Iterable[str]:
    """ Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
     Args: start: Начальное значение диапазона (от 1 до 9999999999999999)
           end: Конечное значение диапазона (от start до 9999999999999999)
    Yields: Строка с номером карты в формате XXXX XXXX XXXX XXXX """

    # Проверка входных данных
    if not (9999999999999999 >= start >= 1):
        raise ValueError("Начальное значение не находится в допустимом диапазоне от 1 до 9999999999999999")
    if not (9999999999999999 >= end >= start):
        raise ValueError("Конечное значение не находится в допустимом диапазоне от начального до 9999999999999999")

    # Генерация номеров карт
    for number in range(start, end + 1):
        # Преобразуем число в строку длинной 16 символов (добавляем нужное количесво нолей в начале)
        card_digits = str(number).zfill(16)
        card_correct = ' '.join([
            card_digits[0:4],
            card_digits[4:8],
            card_digits[8:12],
            card_digits[12:16],
        ])
        yield card_correct

# # Проверим работу фильтра генератора
# for card_number in card_number_generator(1, 5):
#     print(card_number)
