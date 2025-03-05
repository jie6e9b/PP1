from tarfile import TruncatedHeaderError

import pytest

@pytest.fixture
def valid_card_number() -> str:
    """Фикстура для валидного номера карты в виде строки."""
    return "1234567890123456"


@pytest.fixture
def valid_card_number_int() -> int:
    """Фикстура для валидного номера карты в виде целого числа."""
    return 1234567890123456



