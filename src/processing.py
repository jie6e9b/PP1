import re
from collections import Counter
# from typing import Union


def filter_by_state(operations: list, state: str = 'EXECUTED') -> list:
    """ Фильтрует список словарей по значению ключа 'state'.
    Args: list_dict: Список словарей для фильтрации
    state: Значение для фильтрации по ключу 'state' (по умолчанию 'EXECUTED')
    Returns: Отфильтрованный список словарей
    """
    return [operation for operation in operations if operation.get('state') == state]

# print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#                        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}],'EXECUTED'))
#
# print(filter_by_state([{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#                        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],'CANCELED'))
#
# print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#                        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#                        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#                        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
#                       'CANCELED'))


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """ Сортирует список словарей по значению ключа 'date'.
    Args: list_dict: Список словарей для сортировки
    reverse: Порядок сортировки (по умолчанию True - по убыванию)
    Returns: Отсортированный список словарей
    """
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=reverse)

# print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#                     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#                     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#                     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}], True))

# print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#                     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#                     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#                     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], False))


def filter_operations_by_keyword(bank_operations: list[dict], search_string: str) -> list[dict]:
    """ Функция фильтрует список словарей по строке введенной пользователем,
    принимает список словарей с данными о банковских операциях и строку поиска,
    Args: list_dict: Список словарей для фильтрации
          search_string: Строка, введенная пользователем
    Returns: Отфильтрованный список словарей у которых в описании есть данная строка"""
    filtered_operations = [operation for operation in bank_operations
                           if (isinstance(operation.get("description"), str)
                               and re.search(search_string, operation["description"], re.IGNORECASE))]

    return filtered_operations


def count_operations_by_category(bank_operations: list[dict], categories: list[str]) -> dict[str, int]:
    """ Функция, принимает список словарей с данными о банковских операциях и список категорий операций,
    и возвращает возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории. Поиск по описанию операции (по значению ключа "description").
    Args: list_dict: Список словарей для фильтрации
         categories: Строка, список категорий операций
    Returns: Отфильтрованный список словарей у которых список категорий операций"""
    categories_counts = Counter(
        transaction["description"].lower()
        for transaction in bank_operations
        if transaction["description"].lower() in list(map(str.lower, categories)))

    return dict(categories_counts)
