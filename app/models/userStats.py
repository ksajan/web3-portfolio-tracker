from dataclasses import dataclass, field

from solders.pubkey import Pubkey  # type: ignore


@dataclass
class UserFees:
    total_fee_paid: int
    total_fee_rebate: int
    total_token_discount: int
    total_referee_discount: int
    total_referrer_reward: int
    current_epoch_referrer_reward: int


@dataclass
class UserStatsAccount:
    authority: Pubkey
    referrer: Pubkey
    fees: UserFees
    next_epoch_ts: int
    maker_volume30d: int
    taker_volume30d: int
    filler_volume30d: int
    last_maker_volume30d_ts: int
    last_taker_volume30d_ts: int
    last_filler_volume30d_ts: int
    if_staked_quote_asset_amount: int
    number_of_sub_accounts: int
    number_of_sub_accounts_created: int
    is_referrer: bool
    disable_update_perp_bid_ask_twap: bool
    padding: list[int] = field(default_factory=lambda: [0] * 50)
