import os
from typing import List, Dict, Any

from src.generators import filter_by_currency
from src.read_fin_data import read_financial_data
from src.processing import filter_by_state, filter_operations_by_keyword, sort_by_date
from src.utils import read_json_finance
from src.widget import get_date, mask_account_card


# Константы путей к файлам данных с использованием абсолютных путей
PATH_TO_JSON_FILE = os.path.join(os.path.dirname(__file__), "data", "operations.json")
PATH_TO_CSV_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions.csv")
PATH_TO_EXCEL_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions_excel.xlsx")


def main() -> None:
    """ Основная функция управления программой анализа банковских транзакций.
        Последовательно выполняет:
        1. Выбор источника данных (JSON/CSV/XLSX)
        2. Чтение финансовых данных
        3. Фильтрацию и сортировку транзакций по различным параметрам:
            по статусу операции (EXECUTED, CANCELED, PENDING);
            по дате выполнения операции, а также по возрастанию или убыванию даты;
            по коду валюты (RUB, USD, EUR и др.);
            по ключевому слову в описании операции (перевод, открытие вклада и т.д.).    ста
        4. Вывод отфильтрованных транзакций, например:
        --------------------------------------------------
        [1] 15.07.2019 Открытие вклада
        Счет **2265
        Сумма: 92688.46 USD
        -------------------------------------------------- """

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор источника данных с обработкой ошибок
    data_source = get_data_source_selection()

    # Загрузка транзакций из выбранного источника
    transactions = load_transactions(data_source)

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    # Последовательная фильтрация и обработка транзакций
    transactions = process_transactions_filters(transactions)

    # Вывод результатов
    display_transactions(transactions, data_source)

def get_data_source_selection() -> int:
    """ Интерактивный выбор источника данных с валидацией ввода.
        Returns: int: Номер выбранного источника данных (1 - JSON, 2 - CSV, 3 - XLSX) """

    while True:
        try:
            source_choice = int(input(
                "Выберите источник данных:\n"
                "1. JSON-файл\n"
                "2. CSV-файл\n"
                "3. XLSX-файл\n"
                "Введите номер: ").strip())

            if source_choice in [1, 2, 3]:
                return source_choice

            print("Ошибка! Введите 1, 2 или 3.")
        except ValueError:
            print("Ошибка! Требуется ввести число.")
        continue


def load_transactions(source_type: int) -> List[Dict[str, Any]]:
    """ Загрузка транзакций из выбранного источника.
    Args: source_type (int): Тип источника данных
    Returns: List[Dict[str, Any]]: Список транзакций """

    source_map = {
        1: (read_json_finance, PATH_TO_JSON_FILE),
        2: (read_financial_data, PATH_TO_CSV_FILE),
        3: (read_financial_data, PATH_TO_EXCEL_FILE)
    }

    loader, file_path = source_map[source_type]
    print(f"Для обработки выбран {file_path}-файл.")
    return loader(file_path)

def process_transactions_filters(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Последовательная фильтрация транзакций по различным параметрам.
    Args: transactions (List[Dict[str, Any]]): Исходный список транзакций
    Returns: List[Dict[str, Any]]: Отфильтрованный список транзакций"""

    # Фильтрация по статусу
    transactions = filter_transactions_by_status(transactions)

    # Сортировка по дате
    transactions = sort_transactions_by_date(transactions)

    # Фильтрация по валюте
    transactions = filter_transactions_by_currency(transactions)

    # Фильтрация по ключевому слову
    transactions = filter_transactions_by_keyword(transactions)

    return transactions


def filter_transactions_by_status(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Фильтрует транзакции по статусу на основе пользовательского ввода.
    Args: transactions (List[Dict[str, Any]]): Список транзакций для фильтрации
    Returns: List[Dict[str, Any]]: Отфильтрованный список транзакций """
    if not transactions:
        return []

    AVAILABLE_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        user_choice_state = input(
            "Введите статус операции, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтрации статусы: {', '.join(AVAILABLE_STATUSES)}. "
            "Чтобы пропустить этот шаг, введите 'Нет'. "
        ).strip().upper()

        if user_choice_state.lower() == "нет":
            return transactions  # Возвращаем исходный список без фильтрации

        if user_choice_state not in AVAILABLE_STATUSES:
            print(f"Ошибка! Введено неправильное значение. Статус операции '{user_choice_state}' недоступен.")
            continue

        # Фильтрация данных по статусу операций
        filtered_transactions = filter_by_state(transactions, user_choice_state)

        if not filtered_transactions:
            print(f"Транзакции со статусом '{user_choice_state}' не найдены.")
            retry = input("Хотите выбрать другой статус? (да/нет): ").strip().lower()
            if retry == "да":
                continue
            else:
                return transactions  # Возвращаем исходный список, если пользователь не хочет выбирать другой статус

        return filtered_transactions

def sort_transactions_by_date(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Сортирует список транзакций по дате на основе пользовательского выбора.
    Args: transactions (List[Dict[str, Any]]): Список транзакций для сортировки
    Returns: List[Dict[str, Any]]: Отсортированный список транзакций"""
    if not transactions:
        return []

    while True:
        answer_sort_by_date = input("Сортировать операции по дате? (да/нет): ").strip().lower()

        if answer_sort_by_date not in ["да", "нет"]:
            print("Ошибка! Введено неправильное значение. Введите 'да' или 'нет'.")
            continue

        if answer_sort_by_date == "нет":
            return transactions  # Возвращаем исходный список без сортировки

        # Пользователь выбрал сортировку по дате
        while True:
            direction_prompt = (
                "Выберите направление сортировки:\n"
                "В - по возрастанию даты (от старых к новым)\n"
                "У - по убыванию даты (от новых к старым)\n"
                "Введите 'В' или 'У': "
            )
            direction_sort_by_date = input(direction_prompt).strip().upper()

            if direction_sort_by_date not in ["В", "У"]:
                print("Ошибка! Введено неправильное значение. Введите 'В' или 'У'.")
                continue

            # Сортировка данных по выбранному направлению
            is_reverse = direction_sort_by_date == "У"
            sorted_transactions = sort_by_date(transactions, is_reverse)

            print(f"Операции отсортированы по {'убыванию' if is_reverse else 'возрастанию'} даты.")
            return sorted_transactions

def filter_transactions_by_currency(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по выбранной пользователем валюте.
    Args: transactions (List[Dict[str, Any]]): Список транзакций для фильтрации
    Returns: List[Dict[str, Any]]: Отфильтрованный список транзакций """
    if not transactions:
        return []

    while True:
        answer_filter_by_currency = input(
            "Выберите, в какой валюте выводить транзакции (RUB, USD, EUR...).\n"
            "Чтобы пропустить этот шаг, введите 'Нет': "
        ).strip().upper()

        if answer_filter_by_currency.lower() == "нет":
            return transactions  # Возвращаем исходный список без фильтрации

        if len(answer_filter_by_currency) != 3 or not answer_filter_by_currency.isalpha():
            print("Ошибка! Код валюты должен состоять из трех букв (например, RUB, USD, EUR).")
            continue

        # Фильтрация транзакций по выбранной валюте
        filtered_transactions = list(filter(
            lambda transaction: transaction is not None,
            filter_by_currency(transactions, answer_filter_by_currency)
        ))

        if not filtered_transactions:
            print(f"Транзакций в валюте {answer_filter_by_currency} не найдено. Попробуйте другую валюту.")
            continue

        print(f"Найдено {len(filtered_transactions)} транзакций в валюте {answer_filter_by_currency}.")
        return filtered_transactions

def filter_transactions_by_keyword(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """ Фильтрует список транзакций по ключевому слову в описании операции.
    Args: transactions (List[Dict[str, Any]]): Список транзакций для фильтрации
    Returns: List[Dict[str, Any]]: Отфильтрованный список транзакций """
    if not transactions:
        return []

    while True:
        answer_filter_by_keyword = input(
            "Сортировать операции по определенному слову в описании? Да/Нет: ").strip().lower()

        if answer_filter_by_keyword not in ["да", "нет"]:
            print("Ошибка! Введено неправильное значение. Введите 'Да' или 'Нет'.")
            continue

        if answer_filter_by_keyword == "нет":
            return transactions  # Возвращаем исходный список без фильтрации

        # Пользователь выбрал фильтрацию по ключевому слову
        keyword = input("Введите слово для поиска: ").strip()

        if not keyword:
            print("Ошибка! Ключевое слово не может быть пустым.")
            continue

        filtered_transactions = filter_operations_by_keyword(transactions, keyword)

        if not filtered_transactions:
            print(f"Транзакций с ключевым словом '{keyword}' в описании не найдено.")
            retry = input("Хотите попробовать другое ключевое слово? Да/Нет: ").strip().lower()
            if retry == "да":
                continue
            return transactions  # Возвращаем исходный список, если пользователь не хочет продолжать поиск

        print(f"Найдено {len(filtered_transactions)} транзакций с ключевым словом '{keyword}' в описании.")
        return filtered_transactions


def display_transactions(transactions: List[Dict[str, Any]], data_source: int) -> None:
    """ Отображает список транзакций в удобочитаемом формате.
    Args: transactions (List[Dict[str, Any]]): Список транзакций для отображения
          data_source (int): Формат исходного файла ('JSON' - 1, 'CSV' - 2 или 'XLSX' - 3)"""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}.")
    print("-" * 50)

    for index, transaction in enumerate(transactions, 1):
        description = transaction.get('description', '')
        date = get_date(transaction.get('date', ''))
        to_account = mask_account_card(transaction.get('to', ''))

        # Заголовок транзакции с номером
        print(f"[{index}] {date} {description}")

        # Обработка перевода (с указанием счета отправителя и получателя)
        if "перевод" in description.lower():
            from_account = mask_account_card(transaction.get('from', ''))
            print(f"{from_account} -> {to_account}")
        else:
            print(f"{to_account}")

        # Получение суммы и валюты в зависимости от формата файла
        if data_source == 1:
            amount = transaction.get('operationAmount', {}).get('amount', 0)
            currency = transaction.get('operationAmount', {}).get('currency', {}).get('name', '')
        else:  # CSV или XLSX
            amount = transaction.get('amount', 0)
            currency = transaction.get('currency_name', '')

        print(f"Сумма: {amount} {currency}")
        print("-" * 50)  # Разделитель между транзакциями

if __name__ == "__main__":
    main()


