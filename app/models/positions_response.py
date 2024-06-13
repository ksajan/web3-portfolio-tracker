from typing import List, Optional

from pydantic import BaseModel


class ResponsePerpPosition(BaseModel):
    id: str  # Market Index
    account: str  # address of account
    price: float  # current price
    margin_usd: float  # margin amount in USD
    margin_base: float  # margin amount in base currency
    notional_usd: float  # notional amount in USD
    notional_base: float  # notional amount in base currency
    liquidation_price: float  # liquidation price
    symbol: str
    side: str  # short or long
    category: str = "exposure"
    type: str = "perp"
    chain: str = "Solana"  # blockchain
    platform: str = "Drift"
    comment: str = "Drift perp position"


class ResponseSpotPosition(BaseModel):
    id: str
    account: str
    price: float
    margin_usd: float
    margin_base: float
    notional_usd: float
    notional_base: float
    liquidation_price: float
    symbol: str
    side: str  # short or long
    category: str = "spot"
    type: str = "spot"
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift collateral"


class ResponseUnrealizedPnLPosition(BaseModel):
    id: str
    account: str
    price: float
    margin_usd: float
    margin_base: float
    notional_usd: float
    notional_base: float
    liquidation_price: float
    symbol: str
    side: str
    category: str = "both"
    type: str = "spot"
    chain: str = "Solana"
    platform: str = "Drift"
    comment: str = "Drift UPnL"
