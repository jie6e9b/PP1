import functools
import sys
from typing import Any, Callable, Optional, TypeVar, cast, Union, TextIO
F = TypeVar('F', bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """ Декоратор для логирования выполнения функций.
    Args: filename: Имя файла для записи логов. Если None, логи выводятся в консоль.
    Returns: Декорированная функция. """
    def decorator(func: F) -> F:
        @functools.wraps(func)  # Сохраняем метаданные оригинальной функции
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем, куда выводить логи
            log_output: Union[TextIO, None] = None
            try:
                # если аргумент filename задан, значение переменной log_output
                if filename:
                    log_output = open(filename, 'a')
                # если аргумент filename не задан, присваиваем значение переменной log_output
                else:
                    log_output = sys.stdout
                try:
                    # Выполняем функцию
                    result = func(*args, **kwargs)
                    # Логируем, успешное выполнение
                    log_output.write(f"{func.__name__} ok\n")
                    return result
                except Exception as e:
                    # Логируем, ошибку
                    log_output.write(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n")
                    raise
            finally:
                # Закрываем файл, если он был открыт
                if filename and log_output and log_output != sys.stdout:
                    log_output.close()

        return cast(F, wrapper)

    return decorator

#
# @log(filename="mylog.txt")
# def my_function(x, y):
#     return x + y
#
#
# my_function(1, 2)
