from typing import Optional
from masks import get_mask_card_number, get_mask_account

def mask_account_card(paymetn_str_data: Optional[str]) -> Optional[str]:
    """Принимает на вход либо тип карты и ее номер;
                         либо счет карты и ее номер,
    в ответ выдает либо тип и замаскировнный get_mask_card_number номер;
                   либо счет и замаскированный get_mask_account номер
    Пример для карты
    Args: Visa Platinum 7000792289606361 # входной аргумент
    Returns: Visa Platinum 7000 79** **** 6361 # выход функции
    Пример для счета
    Args: Счет 73654108430135874305 # входной аргумент
    Returns: Счет **4305 # выход функции """

    if paymetn_str_data is None:
        return None

    part_account_slpit = paymetn_str_data.split()
    if part_account_slpit[0] == "Счет":
        masked_number = get_mask_account(part_account_slpit[1])
        return f"Счет {masked_number}"
    else:

        card_number = part_account_slpit[-1]
        card_type = ' '.join(part_account_slpit[:-1])
        masked_number = get_mask_card_number(card_number)
        return f"{card_type} {masked_number}"


print(mask_account_card("Счет 35383033474447895560"))


def get_date(date_str: Optional[str]) -> Optional[str]:
    """Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.
    Args:date_str: Строка с датой в формате "ГГГГ-ММ-ДДTчч:мм:сс.мс"
    Returns: Строка с датой в формате "ДД.ММ.ГГГГ" или None  при некорректных данных
    Example: >>> get_date("2024-03-11T02:26:18.671407") ->  "11.03.2024"""

    if date_str is None:
        return None

    if not isinstance(date_str, str):
        return None

    try:
        date_part = date_str.split('T')[0]
        # Разбиваем дату на компоненты
        year, month, day = date_part.split('-')
        # Форматируем дату в нужный формат
        formatted_date = f"{day}.{month}.{year}"

        return formatted_date
    except (ValueError, IndexError):
        return None

print(get_date("2024-03-11T02:26:18.671407"))