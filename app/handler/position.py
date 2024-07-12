from app.models.client_response_types import (
    CustomOnChainPosition,
    CustomPerpPosition,
    CustomSpotPosition,
    CustomUnrealizedPnLPosition,
)
from app.models.response_positions import (
    ResponseOnChainPosition,
    ResponsePerpPosition,
    ResponseSpotPosition,
    ResponseUnrealizedPnLPosition,
)
from app.utils.helper import generate_random_id, generate_uuid


class PositionFactory:
    @staticmethod
    def create_response_perp_position(
        perp_position: CustomPerpPosition, wallet_address: str
    ) -> ResponsePerpPosition:
        return ResponsePerpPosition(
            id=PositionFactory.generate_uuid(
                market_index=perp_position.market_index,
                market_type=perp_position.type,
                symbol=perp_position.symbol,
            ),
            account=wallet_address,
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
            chain=perp_position.chain,
            platform=perp_position.platform,
            comment=perp_position.comment,
        )

    @staticmethod
    def create_response_spot_position(
        spot_position: CustomSpotPosition, wallet_address: str
    ) -> ResponseSpotPosition:
        return ResponseSpotPosition(
            id=PositionFactory.generate_uuid(
                market_index=spot_position.market_index,
                market_type=spot_position.type,
                symbol=spot_position.symbol,
            ),
            account=wallet_address,
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
            chain=spot_position.chain,
            platform=spot_position.platform,
            comment=spot_position.comment,
        )

    @staticmethod
    def create_response_unrealized_pnl_position(
        unrealized_pnl_position: CustomUnrealizedPnLPosition, wallet_address: str
    ) -> ResponseUnrealizedPnLPosition:
        return ResponseUnrealizedPnLPosition(
            id=PositionFactory.generate_uuid(
                market_index=unrealized_pnl_position.market_index,
                market_type=unrealized_pnl_position.type,
                symbol=unrealized_pnl_position.symbol,
            ),
            account=wallet_address,
            price=unrealized_pnl_position.current_price,
            margin_usd=abs(unrealized_pnl_position.pnl),
            margin_base=abs(unrealized_pnl_position.pnl),
            notional_usd=abs(unrealized_pnl_position.pnl),
            notional_base=abs(unrealized_pnl_position.pnl),
            liquidation_price=unrealized_pnl_position.liquidation_price,
            type=unrealized_pnl_position.type,
            symbol=unrealized_pnl_position.symbol,
            side="long" if unrealized_pnl_position.pnl > 0 else "short",
            chain=unrealized_pnl_position.chain,
            platform=unrealized_pnl_position.platform,
            comment=unrealized_pnl_position.comment,
            category=unrealized_pnl_position.category,
        )

    @staticmethod
    def create_response_onchain_position(
        onchain_position: CustomOnChainPosition, wallet_address: str
    ) -> ResponseOnChainPosition:
        return ResponseOnChainPosition(
            id=PositionFactory.generate_random_id(),
            account=wallet_address,
            price=onchain_position.current_price,
            margin_usd=onchain_position.total_price,
            margin_base=onchain_position.amount,
            notional_usd=onchain_position.total_price,
            notional_base=onchain_position.amount,
            liquidation_price=onchain_position.liquidation_price,
            type=onchain_position.type,
            symbol=onchain_position.symbol,
            side=onchain_position.side,
            chain=onchain_position.chain,
            platform=onchain_position.platform,
            comment=onchain_position.comment,
            category=onchain_position.category,
        )

    @staticmethod
    def generate_uuid(market_index: int, market_type: str, symbol: str) -> str:
        return generate_uuid(
            market_index=market_index, market_type=market_type, symbol=symbol
        )

    @staticmethod
    def generate_random_id() -> str:
        return generate_random_id()
