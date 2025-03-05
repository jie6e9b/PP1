from unittest import expectedFailure

import pytest
from typing import Optional, Union, Any
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_with_valid_str(valid_card_number:str) -> None:
    """Тест с валидным строковым номером карты."""
    expected = '1234 56** **** 3456'
    result = get_mask_card_number(valid_card_number)
    assert result == expected


def test_get_mask_card_number_with_valid_int(valid_card_number_int:int) -> None:
    """Тест с валидным челочисленным номером карты"""
    expected = '1234 56** **** 3456'
    result = get_mask_card_number(valid_card_number_int)
    assert result == expected


def test_get_mask_card_number_with_none() -> None:
    """Тест с None в качестве ИД"""
    expected = None
    result = get_mask_card_number(None)  # Передаем None как аргумент
    assert result == expected

@pytest.mark.parametrize(
        "invalid_type",
        [
            1.5,  # float
            [1, 2, 3, 4, 5, 6, 7],  # list
            {"one": 1, "two": 2},  # dictionary
            (1, 2, 3, 4),  # tuple
            True  # bool
        ]
    )

def test_get_mask_card_number_with_invalid_types(invalid_type: Any) -> None:
    """Тест с недопустимыми типами исходных данных"""
    result = get_mask_card_number(invalid_type)
    assert result is None

@pytest.mark.parametrize(
    "invalid_length,expected",
        [
            ("12345", None),  # Слишком короткий
            ("12345678901234567", None),  # Слишком длинный
            ("123456789012345", None),  # На 1 символ короче
            ("12345678901234567890", None),  # Намного длиннее
            (12345, None),  # Целое число неправильной длины
        ]
)

def test_get_mask_card_number_with_invalid_length(invalid_length: Union[str, int], expected: Optional[str]) -> None:
    """Тест с номерами карт неправильной длины."""
    result = get_mask_card_number(invalid_length)
    assert result == expected

@pytest.mark.parametrize(
    "card_number,expected",
        [
            ("1111222233334444", "1111 22** **** 4444"),
            ("9876543210987654", "9876 54** **** 7654"),
            (9999888877776666, "9999 88** **** 6666"),
            (1000000000000001, "1000 00** **** 0001"),
        ]
    )

def test_get_mask_card_number_various_valid_cards(card_number: Union[str, int], expected: str) -> None:
    """Тест с различными валидными номерами карт."""
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_account_with_string_input():
    """Тест маскировки номера счета, переданного в виде строки."""
    account_number = "1234567890123456"
    expected = "**3456"
    result = get_mask_account(account_number)
    assert result == expected

def test_get_mask_account_with_integer_input():
    """Тест маскировки номера счета, переданного в виде целого числа."""
    account_number = 1234567890123456
    expected = "**3456"
    result = get_mask_account(account_number)
    assert result == expected

def test_get_mask_account_with_short_input():
    """Тест маскировки короткого номера счета."""
    account_number = "1234"
    expected = "**1234"
    result = get_mask_account(account_number)
    assert result == expected

def test_get_mask_account_with_none_input():
    """Тест с None в качестве входных данных."""
    account_number = None
    result = get_mask_account(account_number)
    assert result is None

def test_get_mask_account_with_empty_string():
    """Тест с пустой строкой."""
    account_number = ""
    expected = "**"
    result = get_mask_account(account_number)
    assert result == expected
