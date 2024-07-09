from enum import Enum
from typing import Literal

DriftEnv = Literal["devnet", "mainnet"]


class Symbols(Enum):
    UDSC = "UDSC"


class Category(Enum):
    balance = "balance"
    exposure = "exposure"
    both = "both"


class BalanceType(Enum):
    borrow = "borrow"
    deposit = "deposit"


class PositionSide(Enum):
    short = "short"
    long = "long"


class PositionType(Enum):
    perp = "perp"
    spot = "spot"


class Platform(Enum):
    drift = "Drift"
    zeta = "Zeta"
