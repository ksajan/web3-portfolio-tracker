from typing import List

from driftpy.drift_client import DriftClient
from fastapi import HTTPException

from app.models.positions import CustomPerpPosition, ResponsePerpPosition
from app.src.drift.strategy.user_portfolio import UserPortfolio


class Positions:
    def __init__(self, wallet_address: str, drift_client: DriftClient):
        self.positions = []
        self.wallet_address = wallet_address
        self.drift_client = drift_client

    async def initialize_user_portfolio(self):
        if self.drift_client is None:
            raise HTTPException(
                status_code=500, detail="Drift client is not initialized"
            )
        self.user_portfolio = await UserPortfolio.create(
            self.wallet_address, self.drift_client
        )

    def get_perp_markets(self):
        perp_markets = self.user_portfolio.get_all_markets()
        return perp_markets

    def _populate_response_perp_positions(
        self, perp_positions: List[CustomPerpPosition]
    ) -> List[ResponsePerpPosition]:
        response_perp_positions = []
        for perp_position in perp_positions:
            response_perp_position = ResponsePerpPosition(
                id=perp_position.market_index,
                account=self.wallet_address,
                price=perp_position.current_price,
                margin_usd=0.0,
                margin_base=0.0,
                notional_usd=abs(perp_position.base_asset_amount)
                * perp_position.current_price,
                notional_base=abs(perp_position.base_asset_amount),
                liquidation_price=perp_position.liquidation_price,
                category="exposure",
                type="perp",
                symbol=perp_position.symbol,
            )
            response_perp_positions.append(response_perp_position)
        return response_perp_positions

    async def get_all_perp_psoitions(self) -> List[ResponsePerpPosition]:
        perp_positions = await self.user_portfolio.get_user_all_perpetual_positions()
        if perp_positions is not None:
            response = self._populate_response_perp_positions(perp_positions)
            return response
        return []
