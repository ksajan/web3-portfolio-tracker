from pydantic import BaseModel

from app.constants.drift_constants import spot_category


class CustomPerpPosition(BaseModel):
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


class CustomSpotPosition(BaseModel):
    scaled_balance: float
    market_index: int
    symbol: str
    current_price: float
    liquidation_price: float
    type: str = "spot"
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift collateral"
    category: str = spot_category


class CustomUnrealizedPnLPosition(BaseModel):
    pnl: float
    symbol: str  # assuming USDC is used for unrealized PnL
    market_index: int
    current_price: float = 1.0  # using hard coded 1.0 is good enough
    liquidation_price: float = 0.0  # zero for UPnL positions
    type: str = "spot"  # UPnL is a spot position always
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift UPnL"
    category: str = "both"


class CustomOnChainPosition(BaseModel):
    amount: float
    current_price: float
    symbol: str
    total_price: float
    chain: str = "Solana"
    platform: str = "Solana"
    type: str = "spot"
    category: str = "both"
    liquidation_price: float = 0.0
    comment: str = "Solana on-chain position"
    side: str = "long"
