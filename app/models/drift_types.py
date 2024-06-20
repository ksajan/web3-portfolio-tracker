from dataclasses import dataclass
from typing import List, Optional

from app.constants.drift_constants import spot_balance_type, spot_category


@dataclass
class CustomPerpPosition:
    last_cumulative_funding_rate: int
    base_asset_amount: int
    quote_asset_amount: int
    quote_break_even_amount: int
    quote_entry_amount: int
    open_bids: int
    open_asks: int
    settled_pnl: int
    lp_shares: int
    last_base_asset_amount_per_lp: int
    last_quote_asset_amount_per_lp: int
    remainder_base_asset_amount: int
    market_index: int
    symbol: str
    open_orders: int
    per_lp_base: int
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
    open_bids: int
    open_asks: int
    cumulative_deposits: int
    market_index: int
    balance_type: spot_balance_type
    open_orders: int
    symbol: str
    current_price: float
    liquidation_price: float
    padding: Optional[List[int]]
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
