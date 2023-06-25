"""Fixture for testing."""

import pytest


from src.exchange.mt5_exchange import MT5Exchange


@pytest.fixture()
def mt5_exchange() -> MT5Exchange:
    mt5 = MT5Exchange()
    return mt5


@pytest.fixture()
def mt5_mock(mocker):  # type: ignore
    mock_function = mocker.patch("src.exchange.mt5_exchange.connect_to_exchange")
    mock_function.return_value = True
