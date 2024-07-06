from enum import Enum
from typing import Literal

DriftEnv = Literal["devnet", "mainnet"]


class Symbols(Enum):
    UDSC = "UDSC"


class DriftUserPortfolioConstants(Enum):
    spot_category = "spot"
    exposure_category = "exposure"
    both_category = "both"
    borrow_balance = "borrow"
    deposit_balance = "deposit"
    spot_type = "spot"
    perp_type = "perp"
