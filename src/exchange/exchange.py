"""Exchange Protocol Definition"""

from datetime import datetime
from abc import ABC, abstractmethod

import pandas as pd
from src.exchange.constants import TimeFrames


class InvalidTimeFrameError(Exception):
    """Raised when the timeframe is not valid"""

    def __init__(self, message: str = "Invalid Timeframe") -> None:
        super().__init__(message)


class ExchangeEngine(ABC):
    @abstractmethod
    def get_prices(
        self, symbol: str, timeframe: str, time_from: datetime, time_to: datetime
    ) -> pd.DataFrame:
        """Retrieve prices from the exchange"""

    @abstractmethod
    def get_several_asset_prices(
        self, symbols: list[str], timeframe: str, time_from: datetime, time_to: datetime
    ) -> dict[str, pd.DataFrame]:
        """Retrieve prices for several assets from the exchange"""

    @abstractmethod
    def connect_to_exchange(self) -> bool:
        """Connect to the exchange"""

    @abstractmethod
    def disconnect_from_exchange(self) -> None:
        "Disconnect from the exchange"

    def is_timeframe_valid(self, timeframe: str) -> bool:
        """Check if the timeframe is valid"""
        return timeframe in TimeFrames.__members__  # type: ignore
