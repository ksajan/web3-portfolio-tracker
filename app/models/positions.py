from dataclasses import dataclass


@dataclass
class PerpPosition:
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
    open_orders: int
    per_lp_base: int


@dataclass
class ResponsePerpPosition:
    id: int  # Market Index
    account: str  # address of account
    price: float  # current price
    margin_usd: float  # margin amount in USD
    margin_base: float  # 10.0,  # margin amount in base currency
    notional_usd: float  # 4521.0,  # notional amount in USD
    notional_base: float  # 30.0,  # notional amount in base currency
    liquidation_price: float  # 180.6
    category: str = "exposure"
    type: str = "perp"
    chain: str = "Solana"  # blockchain
    platform: str = "Drift"
    symbol: str = "SOL-PERP"
    side: str = "short"  # short or long
    comment: str = "Drift perp position"
