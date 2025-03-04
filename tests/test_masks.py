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
    result = get_mask_card_number() -> None:
    assert result is None


def test_get_mask_card_number_with_invalid_types(invalid_type: Any) -> None:
    """Тест с недопустимыми типами исходных данных"""
    result = get_mask_card_number(invalid_type)
    assert result is None
