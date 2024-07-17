from enum import Enum
from typing import Literal

DriftEnv = Literal["devnet", "mainnet"]


class Symbols(Enum):
    UDSC = "UDSC"


class Category(Enum):
    BALANCE = "balance"
    EXPOSURE = "exposure"
    BOTH = "both"


class BalanceType(Enum):
    BORROW = "borrow"
    DEPOSIT = "deposit"


class PositionSide(Enum):
    SHORT = "short"
    LONG = "long"


class PositionType(Enum):
    PERP = "perp"
    SPOT = "spot"


class Platform(Enum):
    DRIFT = "Drift"
    ZETA = "Zeta"


class Chain(Enum):
    SOLANA = "Solana"
