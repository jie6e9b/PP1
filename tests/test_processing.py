import pytest
from src.processing import filter_by_state, sort_by_date

def test_filter_by_state_executed():
    """Тест фильтрации операций со статусом EXECUTED."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(operations, 'EXECUTED')

    assert len(result) == 2, f"Ожидалось 2 операции, получено {len(result)}"
    assert all(op['state'] == 'EXECUTED' for op in result), "Не все операции имеют статус EXECUTED"
    assert result[0]['id'] == 41428829, "Неверный ID первой операции"
    assert result[1]['id'] == 939719570, "Неверный ID второй операции"


def test_filter_by_state_canceled():
    """Тест фильтрации операций со статусом CANCELED."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(operations, 'CANCELED')

    assert len(result) == 2, f"Ожидалось 2 операции, получено {len(result)}"
    assert all(op['state'] == 'CANCELED' for op in result), "Не все операции имеют статус CANCELED"
    assert result[0]['id'] == 594226727, "Неверный ID первой операции"
    assert result[1]['id'] == 615064591, "Неверный ID второй операции"


def test_filter_by_state_default_parameter():
    """Тест фильтрации с параметром по умолчанию (EXECUTED)."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    ]

    result = filter_by_state(operations)  # Используем параметр по умолчанию

    assert len(result) == 2, f"Ожидалось 2 операции, получено {len(result)}"
    assert all(op['state'] == 'EXECUTED' for op in result), "Не все операции имеют статус EXECUTED"


def test_filter_by_state_empty_list():
    """Тест фильтрации пустого списка."""
    operations = []

    result = filter_by_state(operations, 'EXECUTED')

    assert len(result) == 0, "Ожидался пустой список"
    assert isinstance(result, list), "Результат должен быть списком"


def test_filter_by_state_no_matches():
    """Тест фильтрации, когда нет совпадений."""
    operations = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(operations, 'EXECUTED')

    assert len(result) == 0, "Ожидался пустой список"
    assert isinstance(result, list), "Результат должен быть списком"


def test_filter_by_state_missing_state_key():
    """Тест фильтрации операций с отсутствующим ключом state."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'date': '2018-06-30T02:08:58.425572'},  # Отсутствует ключ state
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    ]

    result = filter_by_state(operations, 'EXECUTED')

    assert len(result) == 1, f"Ожидалась 1 операция, получено {len(result)}"
    assert result[0]['id'] == 41428829, "Неверный ID операции"


def test_sort_by_date_descending():
    """Тест сортировки по дате в порядке убывания (по умолчанию)."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]

    result = sort_by_date(operations)

    assert len(result) == 4, "Количество операций не должно измениться"
    assert result[0]['id'] == 41428829, "Первой должна быть самая новая операция"
    assert result[-1]['id'] == 939719570, "Последней должна быть самая старая операция"

    # Проверяем, что даты действительно отсортированы по убыванию
    dates = [op['date'] for op in result]
    assert dates == sorted(dates, reverse=True), "Даты должны быть отсортированы по убыванию"


def test_sort_by_date_ascending():
    """Тест сортировки по дате в порядке возрастания."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]

    result = sort_by_date(operations, reverse=False)

    assert len(result) == 4, "Количество операций не должно измениться"
    assert result[0]['id'] == 939719570, "Первой должна быть самая старая операция"
    assert result[-1]['id'] == 41428829, "Последней должна быть самая новая операция"

    # Проверяем, что даты действительно отсортированы по возрастанию
    dates = [op['date'] for op in result]
    assert dates == sorted(dates), "Даты должны быть отсортированы по возрастанию"


def test_sort_by_date_empty_list():
    """Тест сортировки пустого списка."""
    operations = []

    result = sort_by_date(operations)

    assert len(result) == 0, "Ожидался пустой список"
    assert isinstance(result, list), "Результат должен быть списком"


def test_sort_by_date_missing_date_key():
    """Тест сортировки операций с отсутствующим ключом date."""
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED'},  # Отсутствует ключ date
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
    ]

    result = sort_by_date(operations)

    assert len(result) == 3, "Количество операций не должно измениться"
    assert result[0]['id'] == 41428829, "Первой должна быть операция с самой новой датой"
    assert result[1]['id'] == 594226727, "Второй должна быть операция со следующей датой"
    assert 'date' not in result[2], "Операция без даты должна быть последней"

