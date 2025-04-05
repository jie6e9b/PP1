import sys
from json import dump
from tempfile import NamedTemporaryFile
from os import unlink
from pathlib import Path
from io import StringIO
from typing import List, Dict, Any
from src.utils import read_json_finance, returns_transaction_amount
from unittest.mock import patch, MagicMock


def test_valid_json_file() -> None:
    """Тестирует функцию read_json_finance с корректным JSON-файлом.
    Создает временный JSON-файл с тестовыми данными, вызывает функцию
    read_json_finance и проверяет, что она корректно считывает и возвращает
    данные из файла. После завершения теста временный файл удаляется. """

    # Создаем временный файл с тестовыми данными
    valid_data: List[Dict[str, Any]] = [
        {"id": 1, "amount": 100, "date": "2023-01-01"},
        {"id": 2, "amount": 200, "date": "2023-01-02"}
    ]

    # Создаем временный файл
    with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        dump(valid_data, temp_file)
        temp_file_path = temp_file.name
        print('------------')
        print(temp_file.name)
        temp_path = Path(temp_file.name)
        print(temp_path.is_file())
    print(temp_path.exists())

    try:
        # Вызываем тестируемую функцию
        result = read_json_finance(temp_file_path)
        # Проверяем результат
        assert result == valid_data, f"Ожидалось {valid_data}, получено {result}"
        print("Тест успешно пройден: чтение корректного JSON-файла")
    finally:
        # Удаляем временный файл
        unlink(temp_file_path)
    print(temp_path.exists())


def test_invalid_json_file() -> None:
    """Тестирует функцию read_json_finance с некорректным JSON-файлом.
    Создает временный файл с некорректными JSON-данными, вызывает функцию
    read_json_finance и проверяет, что она корректно обрабатывает ошибку
    и возвращает пустой список. После завершения теста временный файл удаляется."""

    # Создаем временный файл с некорректными JSON-данными
    invalid_json_content = '{"id": 1, "amount": 100, "date": "2023-01-01", }'
    # Лишняя запятая делает JSON некорректным

    # Создаем временный файл
    with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_file.write(invalid_json_content)
        temp_file_path = temp_file.name
        print('------------')
        print(temp_file.name)
        temp_path = Path(temp_file.name)
        print(temp_path.is_file())
    print(temp_path.exists())

    try:
        # Вызываем тестируемую функцию
        result = read_json_finance(temp_file_path)
        # Проверяем результат - должен быть пустой список из-за некорректного JSON
        assert result == [], f"Ожидался пустой список, получено {result}"
        print("Тест успешно пройден: обработка некорректного JSON-файла")
    finally:
        # Удаляем временный файл
        unlink(temp_file_path)
    print(temp_path.exists())


def test_general_exception_handling() -> None:
    """Тестирует функцию read_json_finance на обработку общего исключения.
    Создает мок-объект для open(), который вызывает исключение при попытке открыть файл.
    Проверяет, что функция корректно обрабатывает исключение и возвращает пустой список."""

    from unittest.mock import patch

    # Определяем функцию, которая будет вызывать исключение
    def mock_open_raising_exception(*args, **kwargs):
        raise Exception("Тестовое исключение")

    # Создаем несуществующий путь к файлу
    test_file_path = "несуществующий_путь.json"

    # Используем patch для замены встроенной функции open на нашу mock-функцию
    with patch('builtins.open', mock_open_raising_exception):
        # Вызываем тестируемую функцию
        result = read_json_finance(test_file_path)

        # Проверяем результат - должен быть пустой список из-за исключения
        assert result == [], f"Ожидался пустой список, получено {result}"

    print("Тест успешно пройден: обработка общего исключения")


def test_nonexistent_file() -> None:
    """Тестирует функцию read_json_finance с несуществующим файлом.
    Проверяет, что функция корректно обрабатывает ситуацию, когда указанный
    файл не существует: возвращает пустой список и выводит соответствующее
    сообщение об ошибке. Для проверки вывода в консоль используется
    перехват стандартного потока вывода. """

    # Путь к несуществующему файлу
    nonexistent_file = "/path/to/nonexistent/file.json"
    # Перехватываем вывод в консоль
    original_stdout = sys.stdout
    sys_stdout = StringIO()
    sys.stdout = sys_stdout  # type: ignore

    try:
        # Вызываем тестируемую функцию
        result = read_json_finance(nonexistent_file)
        # Получаем перехваченный вывод
        output = sys_stdout.getvalue()
        # Проверяем, что функция вернула пустой список
        assert result == [], f"Ожидался пустой список, получено {result}"
        # Проверяем, что было выведено сообщение об ошибке
        assert nonexistent_file in output, (
            f"Ожидалось сообщение об ошибке с упоминанием '{nonexistent_file}'"
        )
        print("Тест успешно пройден: обработка несуществующего файла")
    finally:
        # Восстанавливаем стандартный вывод
        sys.stdout = original_stdout  # type: ignore


@patch('src.utils.os.path.exists')
@patch('src.utils.load_dotenv')
@patch('src.utils.os.getenv')
def test_transaction_in_rubles(
        mock_getenv: MagicMock,
        mock_load_dotenv: MagicMock,
        mock_exists: MagicMock
) -> None:
    """
    Тест проверяет корректность обработки транзакции в рублях.

    Функция должна просто вернуть сумму без конвертации,
    и не должна обращаться к переменным окружения.

    Args:
        mock_getenv: Мок для функции os.getenv
        mock_load_dotenv: Мок для функции load_dotenv
        mock_exists: Мок для функции os.path.exists
    """
    # Подготовка тестовых данных
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "code": "RUB"
            }
        }
    }

    # Вызов тестируемой функции
    result = returns_transaction_amount(transaction)

    # Проверка результата
    assert result == 1000.50

    # Проверка, что функции для работы с .env не вызывались,
    # так как валюта уже в рублях
    mock_exists.assert_not_called()
    mock_load_dotenv.assert_not_called()
    mock_getenv.assert_not_called()


@patch('src.utils.os.path.exists')
@patch('src.utils.load_dotenv')
@patch('src.utils.os.getenv')
@patch('src.utils.requests.request')
def test_transaction_in_foreign_currency(
        mock_request: MagicMock,
        mock_getenv: MagicMock,
        mock_load_dotenv: MagicMock,
        mock_exists: MagicMock
) -> None:
    """Тест проверяет корректность конвертации транзакции в иностранной валюте в рубли.
    Функция должна получить API ключ из переменных окружения,
    выполнить запрос к API для получения курса валют и конвертировать сумму в рубли.
    Args: mock_request: Мок для функции requests.request
        mock_getenv: Мок для функции os.getenv
        mock_load_dotenv: Мок для функции load_dotenv
        mock_exists: Мок для функции os.path.exists"""
    # Подготовка тестовых данных
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Настройка моков
    mock_exists.return_value = True
    mock_getenv.return_value = "fake_api_key"

    # Создаем мок для ответа API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "rates": {
            "RUB": 75.5
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response

    # Вызов тестируемой функции
    result = returns_transaction_amount(transaction)

    # Проверка результата (100 USD * 75.5 = 7550.0 RUB)
    assert result == 7550.00

    # Проверка, что функции для работы с .env вызывались
    mock_exists.assert_called_once()
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_once_with('API_KEY_APILAYER')

    # Проверка вызова API
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert args[0] == "GET"
    assert "https://api.apilayer.com/exchangerates_data/latest" in args[1]
    assert kwargs["headers"] == {"apikey": "fake_api_key"}
    assert kwargs["timeout"] == 10


def test_missing_env_file_in_returns_transaction_amount() -> None:
    """Тестирует функцию returns_transaction_amount на обработку исключения FileNotFoundError
    при отсутствии файла .env.
    Создает мок-объект для os.path.exists(), который возвращает False для проверки пути к .env файлу.
    Проверяет, что функция корректно обрабатывает исключение и возвращает None."""

    from unittest.mock import patch
    import os

    # Тестовая транзакция в валюте, отличной от рублей
    test_transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Функция-заглушка, которая возвращает False для проверки пути к .env файлу
    def mock_path_exists(path):
        # Возвращаем False только для проверки .env файла
        if path.endswith('.env'):
            return False
        # Для всех остальных проверок возвращаем результат реальной функции
        return os.path.exists(path)

    # Используем patch для замены os.path.exists на нашу mock-функцию
    with patch('os.path.exists', mock_path_exists):
        # Вызываем тестируемую функцию
        result = returns_transaction_amount(test_transaction)

        # Проверяем результат - должен быть None из-за исключения FileNotFoundError
        assert result is None, f"Ожидался None, получено {result}"

    print("Тест успешно пройден: обработка отсутствия файла .env в returns_transaction_amount")
