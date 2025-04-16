import logging
import os
import json
import requests
from typing import List, Dict, Any
from typing_extensions import Optional
from dotenv import load_dotenv


# Настройка логгера
def setup_logger():
    """Настраивает и возвращает логгер"""
    # Определяем путь к корню проекта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Предполагаем, что utils.py находится в подпапке проекта

    # Создаем директорию для логов в корне проекта
    log_dir = os.path.join(project_root, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Создаем логгер
    logger = logging.getLogger('utils_logger')
    logger.setLevel(logging.INFO)

    # Очищаем существующие обработчики, если они есть
    if logger.handlers:
        logger.handlers.clear()

    # Формат логов
    log_format = '%(asctime)s - utils.py - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Обработчик для info_utils.log (INFO и WARNING)
    info_handler = logging.FileHandler(os.path.join(log_dir, 'info_utils.log'), mode='w')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    info_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

    # Обработчик для error_utils.log (ERROR и CRITICAL)
    error_handler = logging.FileHandler(os.path.join(log_dir, 'error_utils.log'), mode='w')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger


# Инициализируем логгер
logger = setup_logger()


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
    logger.info(f"Попытка чтения JSON-файла: {path}")

    # Получаем путь к текущему модулю
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше (из src в корень проекта)
    parent_dir = os.path.dirname(current_dir)
    # Формируем полный путь к файлу
    json_path = os.path.join(parent_dir, path)

    logger.info(f"Полный путь к файлу: {json_path}")

    try:
        with open(json_path) as f:
            data = json.load(f)
            # Проверяем, является ли содержимое списком
            if isinstance(data, list):
                logger.info(f"Файл успешно прочитан, получено {len(data)} записей")
                return data
            else:
                logger.warning(f"Файл не содержит список в качестве корневого элемента: {path}")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        print(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Файл содержит некорректный JSON: {path}")
        print(f"Файл содержит некорректный JSON: {path}")
        return []
    except Exception as e:
        logger.critical(f"Произошла непредвиденная ошибка при чтении файла: {e}")
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
        # Проверка входных данных
        if not isinstance(transaction, dict):
            logger.error(f"Неверный тип данных транзакции: {type(transaction)}")
            return None

        logger.info(f"Обработка транзакции: {transaction.get('id', 'unknown_id')}")

        currency = transaction["operationAmount"]["currency"]["code"]
        amount_transaction_currency = float(transaction["operationAmount"]["amount"])

        logger.info(f"Валюта транзакции: {currency}, сумма: {amount_transaction_currency}")

        # Если валюта уже в рублях, просто возвращаем сумму
        if currency == "RUB":
            logger.info(f"Транзакция уже в рублях, возвращаем сумму: {amount_transaction_currency}")
            return amount_transaction_currency

        # Для других валют выполняем конвертацию
        logger.info(f"Требуется конвертация из {currency} в RUB")

        # Загружаем API ключ из .env файла
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        env_path = os.path.join(parent_dir, '.env')

        # Проверяем существование файла .env
        if not os.path.exists(env_path):
            logger.error(f"Файл .env не найден по пути: {env_path}")
            raise FileNotFoundError(f"Файл .env не найден по пути: {env_path}")

        load_dotenv(env_path)
        api_key = os.getenv('API_KEY_APILAYER')
        if not api_key:
            logger.error("API_KEY_APILAYER не найден в файле .env")
            raise ValueError("API_KEY_APILAYER не найден в файле .env")

        # Формируем запрос к API для конвертации валюты
        base_currency = currency
        target_currency = "RUB"
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}&symbols={target_currency}"

        logger.info(f"Отправка запроса к API обмена валют: {url}")

        headers = {"apikey": api_key}
        response = requests.request("GET", url, headers=headers, timeout=10)

        # Проверяем статус ответа
        response.raise_for_status()

        # Парсим результат
        result = response.json()

        exchange_rate = result["rates"]["RUB"]

        logger.info(f"Получен курс обмена: 1 {currency} = {exchange_rate} RUB")

        # Выполняем конвертацию
        amount_in_rub = amount_transaction_currency * exchange_rate
        amount_in_rub_rounded = round(amount_in_rub, 2)  # Округляем до копеек

        logger.info(f"Сумма после конвертации: {amount_in_rub_rounded} RUB")
        return amount_in_rub_rounded

    except KeyError as e:
        logger.error(f"Ошибка в структуре данных транзакции: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении запроса к API: {e}")
        return None
    except json.JSONDecodeError:
        logger.error("Ошибка при разборе ответа API")
        return None
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка при конвертации валюты: {e}")
        return None

# # тестирование работы функции "в ручную"
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
