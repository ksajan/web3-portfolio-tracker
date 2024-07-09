from enum import Enum
from typing import Literal

from .common import BalanceType, Category, PositionType

spot_category = Literal["balance", "exposure", "both"]
spot_balance_type = Literal["borrow", "deposit"]
category = Literal["balance", "exposure", "both"]


class DriftUserPortfolioCategory(Enum):
    spot_category = Category.balance.value
    exposure_category = Category.exposure.value
    both_category = Category.both.value
    balance_category = Category.balance.value


class DriftUserPortfolioBalanceType(Enum):
    borrow_balance = BalanceType.borrow.value
    deposit_balance = BalanceType.deposit.value


class DriftPositionType(Enum):
    spot_type = PositionType.spot.value
    perp_type = PositionType.perp.value


class DriftPositionComment(Enum):
    perp = "Drift perp position"
    spot = "Drift collateral"
    unrealized = "Drift UPnL"
