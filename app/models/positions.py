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
