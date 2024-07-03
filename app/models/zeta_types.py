import typing
from dataclasses import dataclass

from solders.pubkey import Pubkey  # type: ignore
from zetamarkets_py.zeta_client import types


@dataclass
class CrossMarginAccount:
    authority: Pubkey
    delegated_pubkey: Pubkey
    balance: int
    subaccount_index: int
    nonce: int
    force_cancel_flag: bool
    account_type: types.margin_account_type.MarginAccountTypeKind
    open_orders_nonces: list[int]
    open_orders_nonces_padding: list[int]
    rebalance_amount: int
    last_funding_deltas: list[types.anchor_decimal.AnchorDecimal]
    last_funding_deltas_padding: list[types.anchor_decimal.AnchorDecimal]
    product_ledgers: list[types.product_ledger.ProductLedger]
    product_ledgers_padding: list[types.product_ledger.ProductLedger]
    trigger_order_bits: int
    rebate_rebalance_amount: int
    potential_order_loss: list[int]
    potential_order_loss_padding: list[int]
    padding: list[int]
