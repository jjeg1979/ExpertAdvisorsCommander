"""Concrete implementation of the Exchange Protocol"""

from datetime import datetime
import pandas as pd

import yfinance as yf

from src.exchange.exchange import InvalidTimeFrameError, ExchangeEngine

YF_TIMEFRAMES: dict[str, str] = {
    "M1": "1m",
    "M2": "2m",
    "M5": "5m",
    "M15": "15m",
    "M30": "30m",
    "H1": "60m",
    "H1.5": "90m",
    "D1": "1d",
    "D5": "5d",
    "W1": "1wk",
    "MN1": "1mo",
    "MN3": "3mo",
}


class YFinanceExchange(ExchangeEngine):
    def get_prices(
        self, symbol: str, timeframe: str, time_from: datetime, time_to: datetime
    ) -> pd.DataFrame:
        """Get the prices from the YFinance Exchange"""
        if not self.is_timeframe_valid(timeframe):
            raise InvalidTimeFrameError(f"Invalid timeframe: {timeframe}")
        timeframe = YF_TIMEFRAMES[timeframe]
        rates = yf.download(symbol, start=time_from, end=time_to, interval=timeframe)
        return rates

    def get_several_asset_prices(
        self, symbols: list[str], timeframe: str, time_from: datetime, time_to: datetime
    ) -> dict[str, pd.DataFrame]:
        return {
            symbol: self.get_prices(symbol, timeframe, time_from, time_to)
            for symbol in symbols
        }

    def connect_to_exchange(self) -> bool:
        """Connect to the YFinance Exchange"""
        return True

    def disconnect_from_exchange(self) -> None:
        """Disconnect from the YFinance Exchange"""
        return None
