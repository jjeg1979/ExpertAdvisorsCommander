"""Test suite for the exchange module."""


from src.exchange.mt5_exchange import MT5Exchange


class TestMT5Exchange:
    """Test suite for the MT5Exchange class."""

    def test_successful_connection(self, mt5_exchange: MT5Exchange):
        """Test that the connection to the exchange is successful.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The connect_to_exchange method is called.
        THEN: The connection is successful.
        """
        assert mt5_exchange.connect_to_exchange() is True

    # Tests that the timeframe is valid
    def test_valid_timeframe(self, mt5_exchange: MT5Exchange):
        """Test that the timeframe is valid.
        GIVEN: An instance of the MT5Exchange class.
        WHEN: The is_timeframe_valid method is called.
        THEN: The timeframe is valid.
        """
        assert mt5_exchange.is_timeframe_valid("M1") is True
