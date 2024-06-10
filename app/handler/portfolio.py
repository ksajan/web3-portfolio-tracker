from typing import List

from app.constants.drift_constants import drift_perp_markets
from app.models.positions import PerpPosition, ResponsePerpPosition
from app.src.drift.strategy.user_portfolio import UserPortfolio
from app.src.init.service_init import devnet_drift_client, mainnet_drift_client


class Positions:
    def __init__(self, chain_type: str, wallet_address: str):
        self.positions = []
        self.chain_type = chain_type
        self.wallet_address = wallet_address

    def initialize_user_portfolio(self):
        drift_client = (
            mainnet_drift_client
            if self.chain_type == "mainnet"
            else devnet_drift_client
        )
        if drift_client is None:
            raise HTTPException(
                status_code=500, detail="Drift client is not initialized"
            )
        self.user_portfolio = UserPortfolio.create(self.wallet_address, drift_client)

    def get_perp_markets(self):
        perp_markets = self.user_portfolio.get_all_markets()
        return perp_markets

    def get_all_perp_psoitions(self) -> List[ResponsePerpPosition]:
        perp_positions = self.user_portfolio.get_user_all_perpetual_positions(
            self.user_portfolio.drift_user_client_manager
        )
        for perp_position in perp_positions:
            self.positions.append(
                ResponsePerpPosition(
                    id=perp_position.market_index,
                    account=self.wallet_address,
                    price=perp_position.quote_entry_amount,
                    margin_usd=perp_position.quote_entry_amount,
                    margin_base=perp_position.base_asset_amount,
                    notional_usd=perp_position.quote_entry_amount,
                    notional_base=perp_position.base_asset_amount,
                    liquidation_price=perp_position.quote_break_even_amount,
                    symbol=drift_perp_markets[perp_position.market_index],
                    side="short" if perp_position.base_asset_amount < 0 else "long",
                )
            )
