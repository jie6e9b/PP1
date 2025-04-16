import unittest
import os
import pandas as pd
import tempfile
from unittest.mock import patch, MagicMock
from src.read_fin_data import read_financial_data

# Глобальные переменные для тестовых данных
test_data = [
    {'id': 4399167.0, 'state': 'EXECUTED', 'date': '2023-07-08T22:43:16Z',
     'amount': 23949.0, 'currency_name': 'Peso', 'currency_code': 'PHP',
     'from': 'Discover 8086808716905997', 'to': 'Visa 0250616482559995',
     'description': 'Перевод с карты на карту'},
    {'id': 5446796.0, 'state': 'EXECUTED', 'date': '2020-10-06T23:30:05Z',
     'amount': 26873.0, 'currency_name': 'Euro', 'currency_code': 'EUR',
     'from': None, 'to': 'Счет 18984367308636722946', 'description': 'Открытие вклада'},
]


def setup_module():
    """Подготовка тестовых файлов перед запуском тестов"""
    global temp_dir, csv_path, excel_path, empty_csv_path, unsupported_path, test_df

    # Создаем временную директорию
    temp_dir = tempfile.TemporaryDirectory()

    # Создаем тестовый DataFrame
    test_df = pd.DataFrame(test_data)

    # Создаем CSV файл
    csv_path = os.path.join(temp_dir.name, "test.csv")
    test_df.to_csv(csv_path, index=False)

    # Создаем Excel файл
    excel_path = os.path.join(temp_dir.name, "test.xlsx")
    test_df.to_excel(excel_path, index=False)

    # Создаем пустой файл
    empty_csv_path = os.path.join(temp_dir.name, "empty.csv")
    pd.DataFrame().to_csv(empty_csv_path, index=False)

    # Создаем файл с неподдерживаемым расширением
    unsupported_path = os.path.join(temp_dir.name, "test.txt")
    with open(unsupported_path, 'w') as f:
        f.write("test data")


def teardown_module():
    """Очистка после завершения тестов"""
    temp_dir.cleanup()


def test_read_csv_explicit():
    """Тест чтения CSV файла с явным указанием типа"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = test_df
        result = read_financial_data(csv_path, file_type='csv')

        mock_read_csv.assert_called_once()
        assert len(result) == 2
        assert result[0]['amount'] == 23949.0
        assert result[1]['currency_code'] == 'EUR'


def test_read_csv_auto():
    """Тест чтения CSV файла с автоопределением типа"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = test_df
        result = read_financial_data(csv_path)

        mock_read_csv.assert_called_once()
        assert len(result) == 2
        assert result[0]['amount'] == 23949.0


def test_read_excel_explicit():
    """Тест чтения Excel файла с явным указанием типа"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = test_df
        result = read_financial_data(excel_path, file_type='xlsx')

        mock_read_excel.assert_called_once()
        assert len(result) == 2
        assert result[0]['amount'] == 23949.0


def test_read_excel_auto():
    """Тест чтения Excel файла с автоопределением типа"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = test_df
        result = read_financial_data(excel_path)

        mock_read_excel.assert_called_once()
        assert len(result) == 2
        assert result[1]['currency_code'] == 'EUR'


def test_empty_file():
    """Тест чтения пустого файла"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame()
        result = read_financial_data(empty_csv_path)

        assert result == []


def test_file_not_found():
    """Тест обработки несуществующего файла"""
    with patch('os.path.exists', return_value=False):
        result = read_financial_data("non_existent_file.csv")
        assert result == []


def test_csv_exception():
    """Тест обработки исключения при чтении CSV"""
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = Exception("Test exception")
        result = read_financial_data(csv_path)
        assert result == []


def test_excel_exception():
    """Тест обработки исключения при чтении Excel"""
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = Exception("Test exception")
        result = read_financial_data(excel_path)
        assert result == []