from typing import Optional, Union

def get_mask_card_number(card_number: Optional[Union[str, int]]) -> Optional[str]:
    """Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.
    Args: card_number: Номер карты (строка или целое число)
    Returns: Замаскированный номер карты или None при некорректных данных
    Example:  >>> get_mask_card_number(1234567890123456) >>> '1234 56** **** 3456'"""

    # Проверка на None
    if card_number is None:
        return None

    # Проверка типа данных
    if not isinstance(card_number, (str, int)):
        return None

    # Преобразование в строку
    card_str: str = str(card_number)

    # Проверка длины номера карты
    if len(card_str) != 16:
        return None

    # Маскировка номера карты
    masked_number: str = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked_number


def get_mask_account(account_count: Optional[Union[str, int]]) -> Optional[str]:
    """Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.
    Args: account_number: Номер счета (строка или целое число)
    Returns: Замаскированный номер счета или None при некорректных данных
    Example:  >>> get_mask_account(1234567890123456)  >>>  '************ 3456'"""

    # Проверка на None
    if account_count is None:
        return None

    # Проверка типа данных
    if not isinstance(account_count, (str, int)):
        return None

    # Преобразование в строку
    account_count_str: str = str(account_count)

    # Маскировка номера счета
    mask_account: str = f"**{account_count_str[-4:]}"
    return mask_account

