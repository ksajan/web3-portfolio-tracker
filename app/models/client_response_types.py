from dataclasses import dataclass
from typing import List, Optional

from app.constants.drift_constants import spot_balance_type, spot_category


@dataclass
class CustomPerpPosition:
    base_asset_amount: float
    market_index: int
    symbol: str
    current_price: float
    liquidation_price: float
    category: str = "exposure"
    type: str = "perp"
    chain: str = "Solana"  # blockchain
    platform: str = "Drift"
    comment: str = "Drift perp position"


@dataclass
class CustomSpotPosition:
    scaled_balance: int
    market_index: int
    symbol: str
    current_price: float
    liquidation_price: float
    type: str = "spot"
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift collateral"
    category: str = spot_category


@dataclass
class CustomUnrealizedPnLPosition:
    pnl: float
    symbol: str  # assuming USDC is used for unrealized PnL
    type: str
    market_index: int
    current_price: float = 1.0  # using hard coded 1.0 is good enough
    liquidation_price: float = 0.0  # zero for UPnL positions
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift UPnL"
    category: str = "both"
