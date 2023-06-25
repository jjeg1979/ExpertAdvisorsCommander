"""Concrete Implementation of the Exchange Protocol"""

from datetime import datetime
import pandas as pd

import MetaTrader5 as mt5

from src.exchange.constants import TimeFrames

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


class InvalidTimeFrameError(Exception):
    """Raised when the timeframe is not valid"""

    def __init__(self, message: str = "Invalid Timeframe") -> None:
        super().__init__(message)


class MT5Exchange:
    def get_prices(
        self, symbol: str, timeframe: str, time_from: datetime, time_to: datetime
    ) -> pd.DataFrame:
        """Get the prices from the Metatrader Exchange"""
        # TODO: Refactor this function ==> Low cohesion and high coupling
        if not self.connect_to_exchange():
            return pd.DataFrame()
        is_valid_tf = self.is_timeframe_valid(timeframe)
        if not is_valid_tf:
            raise InvalidTimeFrameError()
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
            print("initialize() failed, error code =", mt5.last_error())  # type:ignore
            return False
        return True

    def disconnet_from_exchange(self) -> None:
        """Disconnect from the Metatrader Exchange"""
        if mt5.initialize():  # type:ignore
            mt5.disconnect()  # type:ignore

    def is_timeframe_valid(self, timeframe: str) -> bool:
        """Check if the timeframe is valid"""
        return timeframe in TimeFrames.__members__  # type: ignore
