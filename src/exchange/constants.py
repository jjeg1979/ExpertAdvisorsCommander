"""Contains constants for the exchange module."""

from enum import StrEnum, auto


class TimeFrames(StrEnum):
    """Timeframes available"""

    M1 = auto()
    M2 = auto()
    M3 = auto()
    M4 = auto()
    M5 = auto()
    M15 = auto()
    M30 = auto()
    H1 = auto()
    H2 = auto()
    H4 = auto()
    H8 = auto()
    H12 = auto()
    D1 = auto()
    W1 = auto()
    MN1 = auto()

    def __str__(self) -> str:
        return self.name  # type: ignore
