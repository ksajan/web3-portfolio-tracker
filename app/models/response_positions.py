from pydantic import BaseModel


class ResponsePositionBase(BaseModel):
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
    category: str
    type: str
    chain: str  # blockchain
    platform: str
    comment: str


class ResponsePerpPosition(ResponsePositionBase):
    pass


class ResponseSpotPosition(ResponsePositionBase):
    pass


class ResponseUnrealizedPnLPosition(ResponsePositionBase):
    pass


class ResponseOnChainPosition(ResponsePositionBase):
    pass
