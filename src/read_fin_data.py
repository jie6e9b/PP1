import os
import pandas as pd
from typing import List, Dict, Union
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_financial_data(path: str, file_type: str = 'auto') -> List[Dict]:
    """ Универсальная функция для чтения финансовых операций из различных типов файлов.
    Args:    path (str): Путь к файлу
             file_type (str, optional): Тип файла ('csv', 'xlsx', 'xls', 'auto'). По умолчанию 'auto'
    Returns: List[Dict]: Список словарей с транзакциями """
    try:
        # Определение типа файла
        if file_type == 'auto':
            file_type = path.split('.')[-1].lower()

        # Чтение файла в зависимости от типа
        if file_type == 'csv':
            df = pd.read_csv(path, sep=",|;", engine="python", encoding='utf-8')
        elif file_type in ['xls', 'xlsx']:
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_type}")

        # Проверка на пустоту DataFrame
        if df.empty:
            logger.warning("Файл пуст!")
            return []

        # Очистка данных
        df = df.dropna(how='all')  # Удаление полностью пустых строк

        # Преобразование в список словарей
        transactions = df.to_dict(orient="records")

        logger.info(f"Успешно прочитано {len(transactions)} транзакций из файла {path}")
        return transactions

    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        return []
    except pd.errors.EmptyDataError:
        logger.warning(f"Файл пуст: {path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {path}: {e}")
        return []


# Тест
def main():

    # Путь к файлам данных
    data_folder = 'data/'
    # Получаем путь к текущему модулю
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше (из src в корень проекта)
    parent_dir = os.path.dirname(current_dir)
    # Формируем полный путь к директории с данными
    full_data_path = os.path.join(parent_dir, data_folder)

    # CSV файл
    csv_transactions = read_financial_data(os.path.join(full_data_path, "transactions.csv"))

    # Excel файл
    excel_transactions = read_financial_data(os.path.join(full_data_path, "transactions_excel.xlsx"), file_type='xlsx')

    # Автоматическое определение типа файла
    auto_transactions = read_financial_data(os.path.join(full_data_path, "transactions_excel.xlsx"))

    # Здесь должен быть код для использования полученных данных
    # Например:
    print(f"CSV данные: {len(csv_transactions)} записей")
    print(f"Excel данные: {len(excel_transactions)} записей")
    print(f"Авто-определенные данные: {len(auto_transactions)} записей")
    print(csv_transactions)
if __name__ == "__main__":
    main()