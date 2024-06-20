from enum import Enum
from typing import Literal

spot_category = Literal["balance", "exposure", "both"]
spot_balance_type = Literal["borrow", "deposit"]
category = Literal["balance", "exposure", "both"]


# comments
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


class DriftPositionComment(Enum):
    perp = "Drift perp position"
    spot = "Drift collateral"
    unrealized = "Drift UPnL"
