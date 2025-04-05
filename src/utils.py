import json
import os


def read_json_finance(path: str) -> list:
    """ Читает JSON-файл с финансовыми транзакциями и возвращает их в виде списка словарей.
        Функция преобразует относительный путь в абсолютный, обрабатывает различные
        ошибки чтения файла и проверяет корректность формата данных.
        Args: path (str): Относительный путь к JSON-файлу от корня проекта
                        (например, 'data/operations.json')
        Returns: list: Список словарей с данными о финансовых транзакциях.
                 Возвращает пустой список в случае ошибки или если файл
                 не содержит список в качестве корневого элемента.
        Raises: Исключения не выбрасываются, все ошибки обрабатываются внутри функции
                с выводом сообщений в консоль.
    """
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


result = read_json_finance('data/operations.json')
print("Результат:", result)
