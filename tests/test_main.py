# import os
# import pytest
from unittest.mock import patch  # , mock_open
# from typing import List, Dict, Any
from io import StringIO

from main import (
    get_data_source_selection,
    load_transactions,
    filter_transactions_by_status,
    sort_transactions_by_date,
    filter_transactions_by_currency,
    filter_transactions_by_keyword,
    display_transactions
)

# Тестовые данные
TEST_TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-07-15",
        "description": "Перевод на счет",
        "from": "Счет 1234",
        "to": "Счет 5678",
        "amount": 100.50,
        "currency_name": "USD"
    },
    {
        "id": 2,
        "state": "CANCELED",
        "date": "2020-01-20",
        "description": "Открытие вклада",
        "to": "Счет 9876",
        "amount": 50000.00,
        "currency_name": "RUB"
    }
]


# Тесты для get_data_source_selection
def test_get_data_source_selection_valid_input():
    # Тест корректного ввода
    with patch('builtins.input', return_value='1'):
        assert get_data_source_selection() == 1

    with patch('builtins.input', return_value='2'):
        assert get_data_source_selection() == 2

    with patch('builtins.input', return_value='3'):
        assert get_data_source_selection() == 3


def test_get_data_source_selection_invalid_input():
    # Тест некорректного ввода с последующим корректным вводом
    inputs = ['4', '0', 'abc', '2']
    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = get_data_source_selection()
            assert result == 2
            assert "Ошибка!" in mock_stdout.getvalue()


def test_load_transactions(tmp_path):
    """Тест загрузки транзакций"""
    # Создаем временные файлы для тестирования
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"id": 1, "state": "EXECUTED"}]')

    csv_file = tmp_path / "test.csv"
    csv_file.write_text('id,state\n1,EXECUTED')

    with patch('main.PATH_TO_JSON_FILE', str(json_file)), \
            patch('main.PATH_TO_CSV_FILE', str(csv_file)), \
            patch('main.PATH_TO_EXCEL_FILE', str(tmp_path / "test.xlsx")):
        # Тест JSON
        json_transactions = load_transactions(1)
        assert len(json_transactions) > 0

        # Тест CSV
        csv_transactions = load_transactions(2)
        assert len(csv_transactions) > 0


def test_filter_transactions_by_status():
    """Тест фильтрации транзакций по статусу"""
    # Тест с выполненными транзакциями
    with patch('builtins.input', return_value='EXECUTED'):
        filtered = filter_transactions_by_status(TEST_TRANSACTIONS)
        assert len(filtered) == 1
        assert filtered[0]['state'] == 'EXECUTED'

    # Тест с отмененными транзакциями
    with patch('builtins.input', return_value='CANCELED'):
        filtered = filter_transactions_by_status(TEST_TRANSACTIONS)
        assert len(filtered) == 1
        assert filtered[0]['state'] == 'CANCELED'

    # Тест пропуска фильтрации
    with patch('builtins.input', return_value='Нет'):
        filtered = filter_transactions_by_status(TEST_TRANSACTIONS)
        assert len(filtered) == 2


def test_sort_transactions_by_date():
    """Тест сортировки транзакций по дате"""
    # Сортировка по возрастанию
    with patch('builtins.input', side_effect=['да', 'В']):
        sorted_asc = sort_transactions_by_date(TEST_TRANSACTIONS)
        assert sorted_asc[0]['date'] == '2019-07-15'

    # Сортировка по убыванию
    with patch('builtins.input', side_effect=['да', 'У']):
        sorted_desc = sort_transactions_by_date(TEST_TRANSACTIONS)
        assert sorted_desc[0]['date'] == '2020-01-20'


def test_filter_transactions_by_currency():
    """Тест фильтрации транзакций по валюте"""
    # Фильтрация по USD
    with patch('builtins.input', return_value='USD'):
        filtered_usd = filter_transactions_by_currency(TEST_TRANSACTIONS)
        assert len(filtered_usd) == 1
        assert filtered_usd[0]['currency_name'] == 'USD'

    # Фильтрация по RUB
    with patch('builtins.input', return_value='RUB'):
        filtered_rub = filter_transactions_by_currency(TEST_TRANSACTIONS)
        assert len(filtered_rub) == 1
        assert filtered_rub[0]['currency_name'] == 'RUB'


def test_filter_transactions_by_keyword():
    """Тест фильтрации транзакций по ключевому слову"""
    # Фильтрация по "перевод"
    with patch('builtins.input', side_effect=['да', 'перевод']):
        filtered = filter_transactions_by_keyword(TEST_TRANSACTIONS)
        assert len(filtered) == 1
        assert 'перевод' in filtered[0]['description'].lower()

    # Фильтрация по "вклада"
    with patch('builtins.input', side_effect=['да', 'вклада']):
        filtered = filter_transactions_by_keyword(TEST_TRANSACTIONS)
        assert len(filtered) == 1
        assert 'вклада' in filtered[0]['description'].lower()


def test_display_transactions(capsys):
    """Тест отображения транзакций"""
    display_transactions(TEST_TRANSACTIONS, 2)
    captured = capsys.readouterr()

    assert "Всего банковских операций в выборке: 2" in captured.out
    assert "Перевод на счет" in captured.out
    assert "Открытие вклада" in captured.out


def test_empty_transactions():
    """Тест обработки пустого списка транзакций"""
    # Тесты с пустым списком для каждой функции фильтрации
    assert filter_transactions_by_status([]) == []
    assert sort_transactions_by_date([]) == []
    assert filter_transactions_by_currency([]) == []
    assert filter_transactions_by_keyword([]) == []

    # Тест отображения пустого списка
    with patch('builtins.print') as mock_print:
        display_transactions([], 1)
        mock_print.assert_called_with(
            "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации."
        )
