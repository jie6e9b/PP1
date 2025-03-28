import os
import pytest
from src.decorators import log


def test_log_success_console(capsys):
    """Тест успешного выполнения функции с выводом в консоль."""

    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)

    # Проверяем результат функции
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_error_console(capsys):
    """Тест обработки ошибки с выводом в консоль."""

    @log()
    def divide(x, y):
        return x / y

    # Вызываем функцию, которая вызовет ошибку
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


def test_log_success_file():
    """Тест успешного выполнения функции с записью в файл."""
    test_file = "test_log.txt"

    # Удаляем файл, если он существует
    if os.path.exists(test_file):
        os.remove(test_file)

    @log(filename=test_file)
    def multiply(x, y):
        return x * y

    result = multiply(2, 3)

    # Проверяем результат функции
    assert result == 6

    # Проверяем содержимое файла
    with open(test_file, 'r') as f:
        content = f.read()

    assert "multiply ok" in content

    # Очистка
    os.remove(test_file)


def test_log_error_file():
    """Тест обработки ошибки с записью в файл."""
    test_file = "test_error_log.txt"

    # Удаляем файл, если он существует
    if os.path.exists(test_file):
        os.remove(test_file)

    @log(filename=test_file)
    def access_index(lst, idx):
        return lst[idx]

    # Вызываем функцию, которая вызовет ошибку
    with pytest.raises(IndexError):
        access_index([], 0)

    # Проверяем содержимое файла
    with open(test_file, 'r') as f:
        content = f.read()

    assert "access_index error: IndexError. Inputs: ([], 0), {}" in content

    # Очистка
    os.remove(test_file)
