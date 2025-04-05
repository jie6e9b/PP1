import json
import os
from typing import List, Dict, Any
from typing_extensions import Optional
from dotenv import load_dotenv
import requests


def read_json_finance(path: str) -> List[Dict[str, Any]]:
    """ Читает JSON-файл с финансовыми транзакциями и возвращает их в виде списка словарей.
        Функция преобразует относительный путь в абсолютный, обрабатывает различные
        ошибки чтения файла и проверяет корректность формата данных.
        Args: path (str): Относительный путь к JSON-файлу от корня проекта
                        (например, 'data/operations.json')
        Returns: list: Список словарей с данными о финансовых транзакциях.
                 Возвращает пустой список в случае ошибки или если файл
                 не содержит список в качестве корневого элемента.
        Raises: Исключения не выбрасываются, все ошибки обрабатываются внутри функции
                с выводом сообщений в консоль."""
    # Получаем путь к текущему модулю
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше (из src в корень проекта)
    parent_dir = os.path.dirname(current_dir)
    # Формируем полный путь к файлу
    json_path = os.path.join(parent_dir, path)

    try:
        with open(json_path) as f:
            data = json.load(f)
            # Проверяем, является ли содержимое списком
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Файл содержит некорректный JSON: {path}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

# тестирование работы функции "в ручную"
# result = read_json_finance('data/operations.json')
# print("Результат:", result)


def returns_transaction_amount(transaction: Dict[str, Any]) -> Optional[float]:
    """ Возвращает сумму транзакции в рублях. Если валюта не рубли, конвертирует через API обмена валют.
    Args: transaction: Словарь с данными о транзакции
    Returns: float: Сумма транзакции в рублях или None в случае ошибки"""
    try:
        currency = transaction["operationAmount"]["currency"]["code"]
        amount_transaction_currency = float(transaction["operationAmount"]["amount"])
        # Если валюта уже в рублях, просто возвращаем сумму
        if currency == "RUB":
            return amount_transaction_currency

        # Для других валют выполняем конвертацию
        # Загружаем API ключ из .env файла
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        env_path = os.path.join(parent_dir, '.env')

        # Проверяем существование файла .env
        if not os.path.exists(env_path):
            raise FileNotFoundError(f"Файл .env не найден по пути: {env_path}")

        load_dotenv(env_path)
        api_key = os.getenv('API_KEY_APILAYER')
        if not api_key:
            raise ValueError("API_KEY_APILAYER не найден в файле .env")

        # Формируем запрос к API для конвертации валюты
        base_currency = currency
        target_currency = "RUB"
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}&symbols={target_currency}"

        headers = {"apikey": api_key}
        response = requests.request("GET", url, headers=headers, timeout=10)

        # Проверяем статус ответа
        response.raise_for_status()

        # Парсим результат
        result = response.json()
        exchange_rate = result["rates"]["RUB"]

        # Выполняем конвертацию
        amount_in_rub = amount_transaction_currency * exchange_rate
        return round(amount_in_rub, 2)  # Округляем до копеек

    except KeyError as e:
        print(f"Ошибка в структуре данных транзакции: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса к API: {e}")
        return None
    except json.JSONDecodeError:
        print("Ошибка при разборе ответа API")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при конвертации валюты: {e}")
        return None

# тестирование работы функции "в ручную"
# transaction2 = {
#     "id": 536723678,
#     "state": "EXECUTED",
#     "date": "2018-06-12T07:17:01.311610",
#     "operationAmount": {
#         "amount": "26334.08",
#         "currency": {
#             "name": "EUR",
#             "code": "EUR"
#         }
#     },
#     "description": "Перевод организации",
#     "from": "Visa Classic 4195191172583802",
#     "to": "Счет 17066032701791012883"
# }
# result = returns_transaction_amount(transaction2)
# print(result)
#
