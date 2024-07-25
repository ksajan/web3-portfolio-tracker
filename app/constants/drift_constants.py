from enum import Enum
from typing import Literal

from .common import BalanceType, Category, PositionType

spot_category = Literal["balance", "exposure", "both"]
spot_balance_type = Literal["borrow", "deposit"]
category = Literal["balance", "exposure", "both"]


class DriftUserPortfolioCategory(Enum):
    SPOT_CATEGORY = Category.BALANCE.value
    EXPOSURE_CATEGORY = Category.EXPOSURE.value
    BOTH_CATEGORY = Category.BOTH.value
    BALANCE_CATEGORY = Category.BALANCE.value


class DriftUserPortfolioBalanceType(Enum):
    BORROW_BALANCE = BalanceType.BORROW.value
    DEPOSIT_BALANCE = BalanceType.DEPOSIT.value


class DriftPositionType(Enum):
    SPOT_TYPE = PositionType.SPOT.value
    PERP_TYPE = PositionType.PERP.value


class DriftPositionComment(Enum):
    PERP = "Drift perp position"
    SPOT = "Drift collateral"
    UNREALIZED = "Drift UPnL"


class DriftSubscriptionConfig(Enum):
    POLLING = "polling"
    WEBSOCKET = "websocket"
    CACHED = "cached"
    DEMO = "demo"
