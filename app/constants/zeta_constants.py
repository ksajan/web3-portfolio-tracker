from enum import Enum
from typing import Literal

from .common import BalanceType, Category, PositionType

spot_category = Literal["balance", "exposure", "both"]
spot_balance_type = Literal["borrow", "deposit"]
category = Literal["balance", "exposure", "both"]


class ZetaUserPortfolioCategory(Enum):
    SPOT_CATEGORY = Category.BALANCE.value
    EXPOSURE_CATEGORY = Category.EXPOSURE.value
    BOTH_CATEGORY = Category.BOTH.value
    BALANCE_CATEGORY = Category.BALANCE.value


class ZetaUserPortfolioBalanceType(Enum):
    BORROW_BALANCE = BalanceType.BORROW.value
    DEPOSIT_BALANCE = BalanceType.DEPOSIT.value


class ZetaUserPositionType(Enum):
    SPOT_TYPE = PositionType.SPOT.value
    PERP_TYPE = PositionType.PERP.value


class ZetaUserPositionCommment(Enum):
    SPOT_COMMENT = "Zeta spot position"
    PERP_COMMENT = "Zeta perp position"
    UNREALIZED_PNL_COMMENT = "Zeta unrealized pnl position"
