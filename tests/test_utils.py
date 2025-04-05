import sys
from json import dump
from tempfile import NamedTemporaryFile
from os import unlink
from pathlib import Path
from io import StringIO
from typing import List, Dict, Any
from src.utils import read_json_finance


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
