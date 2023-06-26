"""Fixture for testing."""

import pytest


from src.exchange.mt5_exchange import MT5Exchange
from src.exchange.yf_exchange import YFinanceExchange


@pytest.fixture
def mt5_exchange() -> MT5Exchange:
    mt5 = MT5Exchange()
    return mt5


@pytest.fixture
def yf_exchange() -> YFinanceExchange:
    yf = YFinanceExchange()
    return yf
