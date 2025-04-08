from typing import Optional, Union
import logging
import os


# Настройка логирования
def setup_logger():
    """Настраивает логирование в два файла:
    - info_masks.log для уровней INFO и WARNING
    - error_masks.log для уровней ERROR и CRITICAL
    Файлы перезаписываются при каждом запуске приложения.
    """
    # Создаем директорию для логов, если она не существует
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Очищаем существующие обработчики, если они есть
    if logger.handlers:
        logger.handlers.clear()

    # Форматтер для логов с указанием модуля masks.py
    formatter = logging.Formatter('%(asctime)s - masks.py - %(levelname)s - %(message)s')

    # Обработчик для info_masks.log (INFO и WARNING)
    # Используем 'w' для перезаписи файла при каждом запуске
    info_handler = logging.FileHandler(
        os.path.join(log_dir, 'info_masks.log'),
        mode='w'
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    info_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

    # Обработчик для error_masks.log (ERROR и CRITICAL)
    # Используем 'w' для перезаписи файла при каждом запуске
    error_handler = logging.FileHandler(
        os.path.join(log_dir, 'error_masks.log'),
        mode='w'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger


# Инициализация логгера
logger = setup_logger()


def get_mask_card_number(card_number: Optional[Union[str, int]]) -> Optional[str]:
    """Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.
    Args: card_number: Номер карты (строка или целое число)
    Returns: Замаскированный номер карты или None при некорректных данных
    Example:  >>> get_mask_card_number(1234567890123456) >>> '1234 56** **** 3456'"""

    logger.info(f"Попытка маскировки номера карты: {type(card_number)}")

    # Проверка на None
    if card_number is None:
        logger.warning("Получен None вместо номера карты")
        return None

    # Проверка типа данных
    if not isinstance(card_number, (str, int)):
        logger.error(f"Неверный тип данных для номера карты: {type(card_number)}")
        return None

    # Преобразование в строку
    card_str: str = str(card_number)

    # Проверка длины номера карты
    if len(card_str) != 16:
        logger.warning(f"Некорректная длина номера карты: {len(card_str)}")
        return None

    # Маскировка номера карты
    masked_number: str = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked_number


def get_mask_account(account_count: Optional[Union[str, int]]) -> Optional[str]:
    """Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.
    Args: account_number: Номер счета (строка или целое число)
    Returns: Замаскированный номер счета или None при некорректных данных
    Example:  >>> get_mask_account(1234567890123456)  >>>  '************ 3456'"""

    logger.info(f"Попытка маскировки номера счета: {type(account_count)}")

    # Проверка на None
    if account_count is None:
        logger.warning("Получен None вместо номера счета")
        return None

    # Проверка типа данных
    if not isinstance(account_count, (str, int)):
        logger.error(f"Неверный тип данных для номера счета: {type(account_count)}")
        return None

    # Преобразование в строку
    account_count_str: str = str(account_count)

    # Маскировка номера счета
    mask_account: str = f"**{account_count_str[-4:]}"
    logger.info("Номер счета успешно замаскирован")
    return mask_account
