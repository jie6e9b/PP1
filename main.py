import os

from src.generators import filter_by_currency
from src.read_fin_data import read_financial_data
from src.processing import filter_by_state, filter_operations_by_keyword, sort_by_date
from src.utils import read_json_finance
from src.widget import get_date, mask_account_card


PATH_TO_JSON_FILE = os.path.join(os.path.dirname(__file__), "data", "operations.json")  # Путь к JSON-файлу
PATH_TO_CSV_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions.csv")  # Путь к CSV-файлу
PATH_TO_EXCEL_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions_excel.xlsx")  # Путь к Excel-файлу


def main() -> None:
    """ Главная функция, отвечающая за основную логику проекта и связывающая его функциональности между собой.
    Осуществляет взаимодействие с пользователем, получая от него исходные данные для анализа информации о банковских
    операциях.
    Реализует следующие возможности:
    - чтение данных о банковских операциях из различных источников (JSON, CSV или Excel-файла);
    - фильтрацию данных по статусу операции (EXECUTED, CANCELED, PENDING);
    - фильтрацию данных по дате выполнения операции, а также по возрастанию или убыванию даты;
    - фильтрацию данных по коду валюты (RUB, USD, EUR и др.);
    - фильтрацию данных по ключевому слову в описании операции (перевод, открытие вклада и т.д.).
    Выводит итоговую информацию в следующем формате:
        08.12.2019 Открытие вклада
        Счет **4321
        Сумма: 40542 руб.

        12.11.2019 Перевод с карты на карту
        MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203
        Сумма: 130 USD
    """

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        try:
            answer_get_data_from = int(input("Для начала работы выберите необходимый пункт меню:\n"
                                             "1. Получить информацию о транзакциях из JSON-файла\n"
                                             "2. Получить информацию о транзакциях из CSV-файла\n"
                                             "3. Получить информацию о транзакциях из XLSX-файла\n"
                                             "Введите 1, 2 или 3: ").replace(" ", ""))  # Удаление
            # пробелов, приведение к типу 'int' для проверки наличия нечисловых символов через обработку исключений
            if answer_get_data_from not in [1, 2, 3]:
                print("Ошибка! Введено значение вне указанного диапазона.")
                continue
        except ValueError:
            print(f"Ошибка! Введено нечисловое значение: {answer_get_data_from}.")
            continue
        else:
            break

    selected_file = {1: "JSON", 2: "CSV", 3: "XLSX"}
    print(f"Для обработки выбран {selected_file[answer_get_data_from]}-файл.")

    if selected_file[answer_get_data_from] == "JSON":
        transactions = read_json_finance(PATH_TO_JSON_FILE)  # Получение данных для дальнейшего анализа из JSON-файла
    elif selected_file[answer_get_data_from] == "CSV":
        transactions = get_data_csv(PATH_TO_CSV_FILE)  # Получение данных для дальнейшего анализа из CSV-файла
    elif selected_file[answer_get_data_from] == "XLSX":
        transactions = get_data_excel(PATH_TO_EXCEL_FILE)  # Получение данных для дальнейшего анализа из Excel-файла

    if transactions:  # Если есть данные для дальнейшего анализа
        # Запрос от пользователя команды на фильтрацию данных по статусу операции
        while True:
            answer_filter_by_state = input("Введите статус операции, по которому необходимо выполнить фильтрацию.\n"
                                           "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING. "
                                           "Чтобы пропустить этот шаг, введите 'Нет'. ").replace(" ", "")
            if answer_filter_by_state.lower() == "нет":
                break  # Пользователь прерывает процесс фильтрации данных по статусу операции
            elif answer_filter_by_state.upper() not in ["EXECUTED", "CANCELED", "PENDING"]:
                print(f"Ошибка! Введено неправильное значение. Статус операции '{answer_filter_by_state}' недоступен.")
                continue
            else:
                transactions = filter_by_state(transactions,
                                               answer_filter_by_state)  # Фильтрация данных по статусу операций
                break

    if transactions:  # Если есть данные для дальнейшего анализа
        # Запрос от пользователя команды на фильтрацию данных по дате выполнения операции
        while True:
            answer_sort_by_date = input("Сортировать операции по дате? Да/Нет: ").replace(" ", "")
            if answer_sort_by_date.lower() not in ["да", "нет"]:
                print("Ошибка! Введено неправильное значение. Введите 'Да' или 'Нет'.")
                continue
            elif answer_sort_by_date.lower() == "нет":
                break  # Пользователь прерывает процесс фильтрации данных по дате
            elif answer_sort_by_date.lower() == "да":  # Далее - уточнение запроса о сортировке данных по дате
                while True:
                    direction_sort_by_date = input("Сортировать операции по возрастанию (В) или убыванию (У) даты?\n"
                                                   "Введите 'В' или 'У': ").replace(" ", "")
                    if direction_sort_by_date.upper() not in ["В", "У"]:
                        print("Ошибка! Введено неправильное значение.")
                        continue
                    elif direction_sort_by_date.upper() == "В":  # Сортировка данных по возрастанию даты
                        transactions = sort_by_date(transactions, False)
                        break
                    elif direction_sort_by_date.upper() == "У":  # Сортировка данных по убыванию даты
                        transactions = sort_by_date(transactions, True)
                        break
            break  # Прерывание цикла запроса от пользователя команды на фильтрацию данных по дате

    if transactions:  # Если есть данные для дальнейшего анализа
        # Запрос от пользователя команды на фильтрацию данных по коду валюты
        while True:
            answer_filter_by_currency = input("Выберите, в какой валюте выводить транзакции (RUB, USD, EUR...).\n"
                                              "Чтобы пропустить этот шаг, введите 'Нет'. ").replace(" ", "")
            if answer_filter_by_currency.lower() == "нет":
                break  # Пользователь прерывает процесс фильтрации данных по валюте
            elif len(answer_filter_by_currency) != 3 or not answer_filter_by_currency.isalpha():  # Если количество
                # символов не равно 3 и они - не буквы, запрос повторяется
                print("Ошибка! Введено некорректное значение кода валюты.")
                continue
            else:
                # Выполнение фильтрации данных по коду валюты
                transactions_generator = filter_by_currency(transactions, answer_filter_by_currency)
                # Формирование отфильтрованного по коду валюты списка транзакций, удаление из него значений None
                transactions = [transaction for transaction in transactions_generator if transaction is not None]
                break

    if transactions:  # Если есть данные для дальнейшего анализа
        # Запрос от пользователя команды на фильтрацию данных по ключевому слову в описании
        while True:
            answer_filter_by_keyword = input("Сортировать операции по определенному слову в описании? Да/Нет: "
                                             ).replace(" ", "")
            if answer_filter_by_keyword.lower() not in ["да", "нет"]:
                print("Ошибка! Введено неправильное значение. Введите 'Да' или 'Нет'.")
                continue
            elif answer_filter_by_keyword.lower() == "нет":
                break  # Пользователь прерывает процесс фильтрации данных по ключевому слову
            elif answer_filter_by_keyword.lower() == "да":  # Далее - запрос ключевого слова для поиска
                while True:
                    keyword = input("Введите слово для поиска: ")
                    transactions = filter_operations_by_keyword(transactions, keyword)  # Фильтрация данных
                    # по ключевому слову в описании
                    break
            break

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Распечатываю итоговый список транзакций...\nВсего банковских операций в выборке: {len(transactions)}.")

        # Далее из-за различия в структуре данных у файлов CSV, XLSX и JSON код вывода итоговой информации различается
        # Вывод результатов обработки JSON-файла
        if selected_file[answer_get_data_from] == "JSON":
            for transaction in transactions:
                if "перевод" in transaction.get('description', '').lower():
                    print(f"{get_date(transaction.get('date', ''))} {transaction.get('description', '')}\n"
                          f"{mask_account_card(transaction.get('from', ''))} -> "
                          f"{mask_account_card(transaction.get('to', ''))}\n"
                          f"Сумма: {transaction.get('operationAmount', {}).get('amount', 0)}"
                          f" {transaction.get('operationAmount', {}).get('currency', {}).get('name')}\n")
                else:
                    print(f"{get_date(transaction.get('date', ''))} {transaction.get('description', '')}\n"
                          f"{mask_account_card(transaction.get('to', ''))}\n"
                          f"Сумма: {transaction.get('operationAmount', {}).get('amount', 0)} "
                          f"{transaction.get('operationAmount', {}).get('currency', {}).get('name')}\n")

        # Вывод результатов обработки CSV и XLSX-файлов
        elif selected_file[answer_get_data_from] in ["CSV", "XLSX"]:
            for transaction in transactions:
                if "перевод" in transaction.get('description', '').lower():
                    print(f"{get_date(transaction.get('date', ''))} {transaction.get('description', '')}\n"
                          f"{mask_account_card(transaction.get('from', ''))} -> "
                          f"{mask_account_card(transaction.get('to', ''))}\n"
                          f"Сумма: {transaction.get('amount', 0)} {transaction.get('currency_name')}\n")
                else:
                    print(f"{get_date(transaction.get('date', ''))} {transaction.get('description', '')}\n"
                          f"{mask_account_card(transaction.get('to', ''))}\n"
                          f"Сумма: {transaction.get('amount', 0)} {transaction.get('currency_name')}\n")


if __name__ == "__main__":
    main()


