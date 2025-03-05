import pytest
from src.widget import mask_account_card, get_date


def test_mask_account_card_with_card():
    """Тест маскировки номера карты Visa."""
    input_data = "Visa Platinum 7000792289606361"
    expected = "Visa Platinum 7000 79** **** 6361"
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_with_mastercard():
    """Тест маскировки номера карты MasterCard."""
    input_data = "MasterCard 5555555555554444"
    expected = "MasterCard 5555 55** **** 4444"
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_with_account():
    """Тест маскировки номера счета."""
    input_data = "Счет 73654108430135874305"
    expected = "Счет **4305"
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_with_short_account():
    """Тест маскировки короткого номера счета."""
    input_data = "Счет 1234"
    expected = "Счет **1234"
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_with_none():
    """Тест с None в качестве входных данных."""
    result = mask_account_card(None)
    assert result is None


def test_mask_account_card_with_empty_string():
    """Тест с пустой строкой в качестве входных данных."""
    result = mask_account_card("")
    assert result == ""


# def test_mask_account_card_with_no_card_number():
#     """Тест со строкой без номера карты."""
#     input_data = "Visa Platinum"
#     result = mask_account_card(input_data)
#     assert result == input_data


# def test_mask_account_card_with_invalid_format():
#     """Тест с неправильным форматом входных данных."""
#     input_data = "Неправильный формат 1234567890123456"
#     result = mask_account_card(input_data)
#     assert result == input_data


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ("Visa Gold 7305799447374042", "Visa Gold 7305 79** **** 4042"),
        ("Visa Classic 2842878893689012", "Visa Classic 2842 87** **** 9012"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Maestro 6762820862930043", "Maestro 6762 82** **** 0043"),
        ("МИР 5211277418228469", "МИР 5211 27** **** 8469")
    ]
)
def test_mask_account_card_various_inputs(input_data: str, expected: str):
    """Тест с различными типами карт и счетов."""
    result = mask_account_card(input_data)
    assert result == expected


# def test_mask_account_card_with_extra_spaces():
#     """Тест с дополнительными пробелами во входных данных."""
#     input_data = "Visa  Platinum   7000792289606361"
#     expected = "Visa  Platinum   7000 79** **** 6361"
#     result = mask_account_card(input_data)
#     assert result == expected


def test_mask_account_card_with_lowercase():
    """Тест с входными данными в нижнем регистре."""
    input_data = "visa platinum 7000792289606361"
    expected = "visa platinum 7000 79** **** 6361"
    result = mask_account_card(input_data)
    assert result == expected


def test_mask_account_card_with_mixed_case():
    """Тест с входными данными в смешанном регистре."""
    input_data = "ViSa PlAtInUm 7000792289606361"
    expected = "ViSa PlAtInUm 7000 79** **** 6361"
    result = mask_account_card(input_data)
    assert result == expected


def test_valid_iso_date():
    """Тест преобразования корректной ISO даты."""
    iso_date = "2024-03-11T02:26:18.671407"
    expected = "11.03.2024"
    assert get_date(iso_date) == expected, f"Ожидалось {expected}, получено {get_date(iso_date)}"


def test_valid_iso_date_without_milliseconds():
    """Тест преобразования ISO даты без миллисекунд."""
    iso_date = "2024-03-11T02:26:18"
    expected = "11.03.2024"
    assert get_date(iso_date) == expected, f"Ожидалось {expected}, получено {get_date(iso_date)}"


def test_none_input():
    """Тест с None в качестве входных данных."""
    assert get_date(None) is None, "Ожидался None при входном значении None"


# def test_non_string_input():
#     """Тест с нестроковым входным значением."""
#     assert get_date(123) is None, "Ожидался None при числовом входном значении"
#     assert get_date(datetime.now()) is None, "Ожидался None при входном значении datetime"
#     assert get_date(True) is None, "Ожидался None при булевом входном значении"


def test_invalid_format():
    """Тест с некорректным форматом даты."""
    assert get_date("2024/03/11") is None, "Ожидался None при неверном формате даты"
    assert get_date("11.03.2024") is None, "Ожидался None при неверном формате даты"
    assert get_date("not a date") is None, "Ожидался None при неверном формате даты"


def test_incomplete_date():
    """Тест с неполной датой."""
    assert get_date("2024-03") is None, "Ожидался None при неполной дате"
    assert get_date("T02:26:18") is None, "Ожидался None при неполной дате"


def test_edge_cases():
    """Тест граничных случаев."""
    assert get_date("") is None, "Ожидался None при пустой строке"
    assert get_date("2000-01-01T00:00:00") == "01.01.2000", "Неверное преобразование граничной даты"
    assert get_date("2099-12-31T23:59:59") == "31.12.2099", "Неверное преобразование граничной даты"
