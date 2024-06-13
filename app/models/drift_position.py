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


# @dataclass
# class ResponsePerpPosition:
#     id: int  # Market Index
#     account: str  # address of account
#     price: float  # current price
#     margin_usd: float  # margin amount in USD
#     margin_base: float  # 10.0,  # margin amount in base currency
#     notional_usd: float  # 4521.0,  # notional amount in USD
#     notional_base: float  # 30.0,  # notional amount in base currency
#     liquidation_price: float  # 180.6
#     symbol: str
#     side: str  # short or long
#     category: str = "exposure"
#     type: str = "perp"
#     chain: str = "Solana"  # blockchain
#     platform: str = "Drift"
#     comment: str = "Drift perp position"


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


# @dataclass
# class ResponseSpotPosition:
#     id: int
#     account: str
#     price: float
#     margin_usd: float
#     margin_base: float
#     notional_usd: float
#     notional_base: float
#     liquidation_price: float
#     symbol: str
#     side: str  # short or long
#     category: str = spot_category
#     type: str = "spot"
#     chain: str = "Solana"
#     platform: str = "Drift"
#     comment: str = "Drift collateral"


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


# @dataclass
# class ResponseUnrealizedPnLPosition:
#     id: int
#     account: str
#     price: float
#     margin_usd: float
#     margin_base: float
#     notional_usd: float
#     notional_base: float
#     liquidation_price: float
#     symbol: str
#     side: str
#     category: str = "both"
#     type: str = "spot"
#     chain: str = "Solana"
#     platform: str = "Drift"
#     comment: str = "Drift UPnL"


"""
unrealized_pnl_position = {
        # same ID if positions are related,
        # for example perp position and unrealized PnL related to that same position
        # relevant here as unrealized PnL is always related to a perp position
        'id': uuid4(),
        'category': 'both',  # balance positions are both balance and exposure
        'type': 'spot',
        'account': '0x...',  # address of account
        'chain': 'Solana',  # blockchain
        'platform': 'Drift',
        'symbol': 'USDC',  # assuming USDC is used for unrealized PnL
        'price': 1.0,  # using hard coded 1.0 is good enough for stablecoins
        'side': 'long',  # can be long or short
        # margin and notional are same for balance positions
        # base means base currency or SOL in this case
        'margin_usd': 50.4,  # margin amount in USD
        'margin_base': 50.4,  # margin amount in base currency
        'notional_usd': 50.4,  # notional amount in USD
        'notional_base': 50.4,  # notional amount in base currency
        'comment': 'Drift UPnL',
        'liquidation_price': 0.0,  # zero for UPnL positions
}



for spot positions,
margin_base = notional_base = Deposits (earning) from Step Finance (inside Margin Trading section at the bottom there is Your Balances)
Kristjan — Today at 11:35 AM
for upnl positions:
margin_base = notional_base = margin_usd (since USDC is settlement currency) = notional_usd (since USDC is settlement currency)  = Unrealized P&L from Step Finance (Margin Trading -> Positions -> last column there)
"""
