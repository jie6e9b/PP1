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


@pytest.mark.paramitrize("invalid type",
                         [1.5, #float
                         [1, 2, 3, 4, 5, 6, 7], #list
                         {"one":1, "two":2}, #dictionary
                         (1, 2, 3, 4), #tuple
                         True #bool
                         ])
