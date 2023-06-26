"""Concrete Implementation of the Exchange Protocol"""
import logging
from datetime import datetime
import pandas as pd

import MetaTrader5 as mt5

from src.exchange.exchange import ExchangeEngine, InvalidTimeFrameError


MT5_TIMEFRAMES: dict[str, int] = {
    "M1": mt5.TIMEFRAME_M1,
    "M2": mt5.TIMEFRAME_M2,
    "M3": mt5.TIMEFRAME_M3,
    "M4": mt5.TIMEFRAME_M4,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H2": mt5.TIMEFRAME_H2,
    "H4": mt5.TIMEFRAME_H4,
    "H8": mt5.TIMEFRAME_H8,
    "H12": mt5.TIMEFRAME_H12,
    "D1": mt5.TIMEFRAME_D1,
    "W1": mt5.TIMEFRAME_W1,
    "MN1": mt5.TIMEFRAME_MN1,
}


class MT5Exchange(ExchangeEngine):
    def get_prices(
        self, symbol: str, timeframe: str, time_from: datetime, time_to: datetime
    ) -> pd.DataFrame:
        """Get the prices from the Metatrader Exchange"""
        # TODO: Refactor this function ==> Low cohesion and high coupling
        if not self.connect_to_exchange():
            return pd.DataFrame()

        if not self.is_timeframe_valid(timeframe):
            raise InvalidTimeFrameError(f"Invalid timeframe {timeframe}")
        tf_mt5 = MT5_TIMEFRAMES[timeframe]
        rates = mt5.copy_rates_range(  # type: ignore
            symbol, tf_mt5, time_from, time_to
        )  # type: ignore

        return pd.DataFrame(rates)  # type: ignore

    def get_several_asset_prices(
        self, symbols: list[str], timeframe: str, time_from: datetime, time_to: datetime
    ) -> dict[str, pd.DataFrame]:
        return {
            symbol: self.get_prices(symbol, timeframe, time_from, time_to)
            for symbol in symbols
        }

    def connect_to_exchange(self) -> bool:
        """Connect to the Metatrader Exchange"""
        if not mt5.initialize():  # type: ignore
            mt5_error: str = mt5.last_error()  # type: ignore
            logging.info(f"Initialize() failed, error code = {mt5_error}")  # type: ignore
        return True

    def disconnect_from_exchange(self) -> None:
        """Disconnect from the Metatrader Exchange"""
        if mt5.initialize():  # type:ignore
            mt5.disconnect()  # type:ignore
