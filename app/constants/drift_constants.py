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


class DriftUserPortfolioCategory(Enum):
    spot_category = Category.balance
    exposure_category = Category.exposure
    both_category = Category.both
    balance_category = Category.balance


class DriftUserPortfolioBalanceType(Enum):
    borrow_balance = BalanceType.borrow
    deposit_balance = BalanceType.deposit


class DriftPositionType(Enum):
    spot_type = PositionType.spot
    perp_type = PositionType.perp


class DriftUserPortfolioConstants(Enum):
    spot_category = DriftUserPortfolioCategory.spot_category
    exposure_category = DriftUserPortfolioCategory.exposure_category
    both_category = DriftUserPortfolioCategory.both_category
    balance_category = DriftUserPortfolioCategory.balance_category
    borrow_balance = DriftUserPortfolioBalanceType.borrow_balance
    deposit_balance = DriftUserPortfolioBalanceType.deposit_balance
    perp_type = DriftPositionType.perp_type
    spot_type = DriftPositionType.spot_type
    drift_platform = Platform.drift
    perp_comment = DriftPositionComment.perp
    spot_comment = DriftPositionComment.spot
    unrealized_comment = DriftPositionComment.unrealized
