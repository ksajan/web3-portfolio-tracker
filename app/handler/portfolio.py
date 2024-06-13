from typing import Dict, List, Union

from driftpy.drift_client import DriftClient
from fastapi import HTTPException

from app.models.drift_position import (
    CustomPerpPosition,
    CustomSpotPosition,
    CustomUnrealizedPnLPosition,
)
from app.models.positions_response import (
    ResponsePerpPosition,
    ResponseSpotPosition,
    ResponseUnrealizedPnLPosition,
)
from app.src.drift.strategy.user_portfolio import UserPortfolio
from app.utils.helper import generate_uuid


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
        try:
            response_perp_positions = []
            for perp_position in perp_positions:
                response_perp_position = ResponsePerpPosition(
                    id=generate_uuid(
                        market_index=perp_position.market_index,
                        market_type=perp_position.type,
                        symbol=perp_position.symbol,
                    ),
                    account=self.wallet_address,
                    price=perp_position.current_price,
                    margin_usd=0.0,
                    margin_base=0.0,
                    notional_usd=abs(perp_position.base_asset_amount)
                    * perp_position.current_price,
                    notional_base=abs(perp_position.base_asset_amount),
                    liquidation_price=perp_position.liquidation_price,
                    category=perp_position.category,
                    type=perp_position.type,
                    symbol=perp_position.symbol,
                    side="long" if perp_position.base_asset_amount > 0 else "short",
                )
                response_perp_positions.append(response_perp_position)
            return response_perp_positions
        except Exception as e:
            print(f"Error in populating response perp positions: {e}")
            return []

    async def get_all_perp_psoitions(self) -> List[ResponsePerpPosition]:
        perp_positions = await self.user_portfolio.get_user_perpetual_positions()
        if perp_positions is not None:
            response = self._populate_response_perp_positions(perp_positions)
            return response
        return []

    def _populate_response_spot_positions(
        self, spot_positions: List[CustomSpotPosition]
    ) -> List[ResponseSpotPosition]:
        try:
            response_spot_positions = []
            for spot_position in spot_positions:
                response_spot_position = ResponseSpotPosition(
                    id=generate_uuid(
                        market_index=spot_position.market_index,
                        market_type=spot_position.type,
                        symbol=spot_position.symbol,
                    ),
                    account=self.wallet_address,
                    price=spot_position.current_price,
                    margin_usd=0.0,
                    margin_base=0.0,
                    notional_usd=abs(spot_position.scaled_balance)
                    * spot_position.current_price,
                    notional_base=abs(spot_position.scaled_balance),
                    liquidation_price=spot_position.liquidation_price,
                    category=spot_position.category,
                    type=spot_position.type,
                    symbol=spot_position.symbol,
                    side="long" if spot_position.scaled_balance > 0 else "short",
                )
                response_spot_positions.append(response_spot_position)
            return response_spot_positions
        except Exception as e:
            print(f"Error in populating response spot positions: {e}")
            return []

    async def get_all_spot_positions(self):
        spot_positions = await self.user_portfolio.get_user_spot_positions()
        if spot_positions is not None:
            response = self._populate_response_spot_positions(spot_positions)
            return response
        return []

    def _populate_unrealized_pnl_positions(
        self, unrealized_pnl_positions: List[CustomUnrealizedPnLPosition]
    ) -> List[ResponseUnrealizedPnLPosition]:
        try:
            response_unrealized_pnl_positions = []
            for unrealized_pnl_position in unrealized_pnl_positions:
                response_unrealized_pnl_position = ResponseUnrealizedPnLPosition(
                    id=generate_uuid(
                        market_index=unrealized_pnl_position.market_index,
                        market_type=unrealized_pnl_position.type,
                        symbol=unrealized_pnl_position.symbol,
                    ),
                    account=self.wallet_address,
                    price=unrealized_pnl_position.current_price,
                    margin_usd=unrealized_pnl_position.pnl,
                    margin_base=unrealized_pnl_position.pnl,
                    notional_usd=abs(unrealized_pnl_position.pnl),
                    notional_base=abs(unrealized_pnl_position.pnl),
                    liquidation_price=unrealized_pnl_position.liquidation_price,
                    type=unrealized_pnl_position.type,
                    symbol=unrealized_pnl_position.symbol,
                    side="long" if unrealized_pnl_position.pnl > 0 else "short",
                )
                response_unrealized_pnl_positions.append(
                    response_unrealized_pnl_position
                )
            return response_unrealized_pnl_positions
        except Exception as e:
            print(f"Error in populating response unrealized pnl positions: {e}")
            return []

    async def get_all_unrealized_pnl_positions(self):
        unrealized_pnl_positions = await self.user_portfolio.get_user_unrealized_pnl()
        if unrealized_pnl_positions is not None:
            response = self._populate_unrealized_pnl_positions(unrealized_pnl_positions)
            return response
        return []

    async def get_all_positions(
        self,
    ) -> Dict[
        str,
        List[
            Union[
                ResponsePerpPosition,
                ResponseSpotPosition,
                ResponseUnrealizedPnLPosition,
            ]
        ],
    ]:
        await self.initialize_user_portfolio()
        perp_positions = await self.get_all_perp_psoitions()
        spot_positions = await self.get_all_spot_positions()
        unrealized_pnl_positions = await self.get_all_unrealized_pnl_positions()
        return {
            "perp_positions": perp_positions,
            "spot_positions": spot_positions,
            "unrealized_pnl_positions": unrealized_pnl_positions,
        }
