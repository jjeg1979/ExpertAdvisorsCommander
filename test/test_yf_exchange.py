"""Test suite for the YFinanceExchange class."""
from datetime import datetime

import pytest
import pandas as pd
from pytest_mock import MockerFixture

from src.exchange.exchange import InvalidTimeFrameError
from src.exchange.yf_exchange import YFinanceExchange


class TestYahooFinanceExchange:
    """Class test for the Yahoo Finance Exchange functions."""

    def test_get_prices_returns_dataframe(self, yf_exchange: YFinanceExchange) -> None:
        """Test that the get_prices method returns a dataframe.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The get_prices method is called.
        THEN: A dataframe is returned with the correct shape"""
        expected_columns: list[str] = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]
        prices = yf_exchange.get_prices(
            "AAPL", "D1", datetime(2021, 1, 1), datetime(2021, 12, 31)
        )
        assert isinstance(prices, pd.DataFrame)
        assert prices.shape == (251, 6)
        assert prices.columns.tolist() == expected_columns

    def test_get_several_asset_prices_returns_dict_of_dataframes(
        self, mocker: MockerFixture
    ):
        """Test that the get_several_asset_prices method returns a dict of dataframes.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The get_several_asset_prices method is called.
        THEN: A dict of dataframes is returned with the correct shape"""
        yf_exchange = YFinanceExchange()
        mocker.patch.object(yf_exchange, "get_prices", return_value=pd.DataFrame())
        result = yf_exchange.get_several_asset_prices(
            ["AAPL", "GOOG"], "D1", datetime(2022, 1, 1), datetime(2022, 1, 2)
        )
        assert isinstance(result, dict)
        assert all(isinstance(value, pd.DataFrame) for value in result.values())

    def test_get_prices_raises_invalid_timeframe_error(
        self, yf_exchange: YFinanceExchange
    ) -> None:
        """Test that the get_prices method raises an InvalidTimeFrameError.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The get_prices method is called with an invalid timeframe.
        THEN: An InvalidTimeFrameError is raised."""
        with pytest.raises(InvalidTimeFrameError) as exc_info:
            yf_exchange.get_prices(
                "AAPL", "D0", datetime(2021, 1, 1), datetime(2021, 12, 31)
            )
        assert exc_info.type == InvalidTimeFrameError
        assert exc_info.value.args[0] == "Invalid timeframe: D0"

    def test_invalid_timeframe_error_raised_for_invalid_timeframe_in_get_several_asset_prices(
        self, mocker: MockerFixture
    ):
        """Test that the get_several_asset_prices method raises an InvalidTimeFrameError.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The get_several_asset_prices method is called with an invalid timeframe.
        THEN: An InvalidTimeFrameError is raised."""
        yf_exchange = YFinanceExchange()
        mocker.patch.object(yf_exchange, "is_timeframe_valid", return_value=False)
        with pytest.raises(InvalidTimeFrameError) as exc_info:
            yf_exchange.get_several_asset_prices(
                ["AAPL", "GOOG"], "invalid", datetime(2022, 1, 1), datetime(2022, 1, 2)
            )
        assert exc_info.type == InvalidTimeFrameError  # type: ignore
        assert exc_info.value.args[0] == "Invalid timeframe: invalid"

    def test_connect_to_exchange_returns_true(self):
        """Test that the connect_to_exchange method returns True.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The connect_to_exchange method is called.
        THEN: True is returned."""
        yf_exchange = YFinanceExchange()
        result = yf_exchange.connect_to_exchange()
        assert result is True

    def test_disconnect_from_exchange_returns_none(self):
        """Test that the disconnect_from_exchange method returns None.
        GIVEN: An instance of the YFinanceExchange class.
        WHEN: The disconnect_from_exchange method is called.
        THEN: None is returned."""
        yf_exchange = YFinanceExchange()
        assert yf_exchange.disconnect_from_exchange() is None
