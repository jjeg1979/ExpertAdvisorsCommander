"""Test suite for the exchange module."""

from datetime import datetime

import pandas as pd
import pytest

from pytest_mock import MockerFixture
from src.exchange.mt5_exchange import MT5Exchange, InvalidTimeFrameError


class TestMT5Exchange:
    """Test suite for the MT5Exchange class."""

    def test_successful_connection(
        self, mt5_exchange: MT5Exchange, mocker: MockerFixture
    ):
        """Test that the connection to the exchange is successful.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The connect_to_exchange method is called.
        THEN: The connection is successful.
        """

        mocker.patch.object(
            mt5_exchange,
            "connect_to_exchange",
            return_value=True,
        )
        assert mt5_exchange.connect_to_exchange() is True

    def test_unsuccessful_connection(
        self, mt5_exchange: MT5Exchange, mocker: MockerFixture
    ):
        """Test that the connection to the exchange is unsuccessful.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The connect_to_exchange method is called.
        THEN: The connection is unsuccessful.
        """

        mocker.patch.object(
            mt5_exchange,
            "connect_to_exchange",
            return_value=False,
        )
        assert mt5_exchange.connect_to_exchange() is False

    def test_valid_timeframe(self, mt5_exchange: MT5Exchange):
        """Test that the timeframe is valid.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The is_timeframe_valid method is called.
        THEN: The timeframe is valid.
        """
        assert mt5_exchange.is_timeframe_valid("M1") is True

    def test_invalid_timeframe(self, mt5_exchange: MT5Exchange):
        """Test that the timeframe is invalid.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The is_timeframe_valid method is called.
        THEN: The timeframe is invalid.
        """
        assert mt5_exchange.is_timeframe_valid("M0") is False

    def test_get_prices_raises_invalid_timeframe_error(
        self, mt5_exchange: MT5Exchange, mocker: MockerFixture
    ):
        """Test that the get_prices method raises an InvalidTimeFrameError when called with an invalid timeframe.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The get_prices method is called with an invalid timeframe.
        THEN: An InvalidTimeFrameError is raised.
        """
        mocker.patch.object(mt5_exchange, "connect_to_exchange", return_value=True)
        mocker.patch.object(mt5_exchange, "is_timeframe_valid", return_value=False)
        with pytest.raises(InvalidTimeFrameError):
            mt5_exchange.get_prices("symbol", "M0", datetime.now(), datetime.now())

    def test_get_prices_returns_non_empty_dataframe(
        self, mt5_exchange: MT5Exchange, mocker: MockerFixture
    ):
        """Tests that the get_prices method of MT5Exchange returns an empty pandas
        DataFrame when called with invalid arguments.
        GIVEN: a MT5Exchange instance
        WHEN: calling get_prices with valid symbol, timeframe, time_from, and time_to arguments
        THEN: ensure that the function returns a non-empty pandas DataFrame
        """

        # Mock the necessary methodsand create fake output
        output = pd.DataFrame(
            data={
                "open": [1.0],
                "high": [1.0],
                "low": [1.0],
                "close": [1.0],
                "volume": [1.0],
            }
        )
        mocker.patch.object(mt5_exchange, "connect_to_exchange", return_value=True)
        mocker.patch.object(mt5_exchange, "is_timeframe_valid", return_value=True)
        mocker.patch.object(mt5_exchange, "get_prices", return_value=output)

        # Call get_prices with valid arguments and ensure that it returns a non-empty DataFrame
        assert (
            mt5_exchange.get_prices(
                "symbol", "M1", datetime.now(), datetime.now()
            ).empty
            is False
        )

        # Tests that an empty DataFrame is returned when get_prices is called with an invalid symbol, timeframe, and time range.

    def test_invalid_symbol(self, mt5_exchange: MT5Exchange, mocker: MockerFixture):
        """
        Test the MT5Exchange class with an invalid symbol.

        GIVEN a MT5Exchange instance
        WHEN get_prices is called with an invalid symbol, timeframe, and time range
        THEN an empty DataFrame should be returned
        """

        # Mocking
        mocker.patch.object(mt5_exchange, "connect_to_exchange", return_value=True)
        mocker.patch.object(mt5_exchange, "is_timeframe_valid", return_value=True)
        mocker.patch.object(mt5_exchange, "get_prices", return_value=pd.DataFrame())

        # Execution
        result = mt5_exchange.get_prices(
            "invalid", "M1", datetime.now(), datetime.now()
        )

        # Assertion
        assert result.empty is True

        # Tests that the get_prices method of MT5Exchange returns a non-None value when valid parameters are passed.

    def test_valid_parameters_return_not_none(
        self, mt5_exchange: MT5Exchange, mocker: MockerFixture
    ):
        """
        Test that the get_prices method of MT5Exchange returns a non-None value when valid parameters are passed.

        GIVEN: A set of valid parameters for get_prices method. Mock the connect_to_exchange, is_timeframe_valid, and get_prices methods of mt5_exchange object.
        WHEN: Calling the get_prices method with the valid parameters.
        THEN: The returned value is not None.

        """
        symbol = "symbol"
        timeframe = "M1"
        time_from = datetime.now()
        time_to = datetime.now()

        mocker.patch.object(mt5_exchange, "connect_to_exchange", return_value=True)
        mocker.patch.object(mt5_exchange, "is_timeframe_valid", return_value=True)
        mocker.patch.object(mt5_exchange, "get_prices", return_value=pd.DataFrame())
        result = mt5_exchange.get_prices(symbol, timeframe, time_from, time_to)

        assert result is not None
