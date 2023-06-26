"""Exchange Protocol Definition"""

from datetime import datetime
from typing import Protocol

import pandas as pd


class ExchangeEngine(Protocol):
    def get_prices(
        self, symbol: str, timeframe: str, time_from: datetime, time_to: datetime
    ) -> pd.DataFrame:
        """Retrieve prices from the exchange"""

    def get_several_asset_prices(
        self, symbols: list[str], timeframe: str, time_from: datetime, time_to: datetime
    ) -> dict[str, pd.DataFrame]:
        """Retrieve prices for several assets from the exchange"""

    def connect_to_exchange(self) -> bool:
        """Connect to the exchange"""

    def disconnect_from_exchange(self) -> None:
        "Disconnect from the exchange"
