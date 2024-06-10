from typing import List, Optional

from driftpy.constants.numeric_constants import PRICE_PRECISION
from driftpy.drift_client import DriftClient
from driftpy.drift_user import BASE_PRECISION, QUOTE_PRECISION, DriftUser
from driftpy.drift_user_stats import DriftUserStats
from driftpy.types import PerpPosition

from app.models.positions import CustomPerpPosition, ResponsePerpPosition
from app.src.drift.clients.user_client import (
    DriftUserAccountStatsClientManager,
    DriftUserClientManager,
)
from app.src.drift.strategy.drift_strategy import DriftStrategy
from app.src.drift.utils.helper import (
    convert_perp_position_to_response_perp_position,
    filter_fields_for_dataclass,
    update_fields,
)


class UserPortfolio:
    def __init__(
        self,
        user_pubkey: str,
        drift_user_client_manager_object: DriftUserClientManager,
        drift_user_account_stats_client_manager: DriftUserStats,
        drift_strategy_object: DriftStrategy,
    ):
        self.user_pubkey = user_pubkey
        self.drift_user_client_manager_object = drift_user_client_manager_object
        self.drift_user_account_stats_client_manager = (
            drift_user_account_stats_client_manager
        )
        self.drift_strategy_object = drift_strategy_object
        self.current_market_data = None

    async def get_current_market_data(self):
        all_markets = await self.drift_strategy_object.get_markets()
        self.current_market_data = all_markets

    @classmethod
    async def create(cls, user_pubkey: str, drift_client: DriftClient):
        try:
            drift_user_client_manager_object = DriftUserClientManager(
                user_pubkey, drift_client
            )
            drift_user_account_stats_client_manager_object = (
                DriftUserAccountStatsClientManager(user_pubkey, drift_client)
            )
            drift_user_account_stats_client_manager = (
                await drift_user_account_stats_client_manager_object.get_user_stats_account_client()
            )

            drift_strategy_object = DriftStrategy(drift_client)
            return cls(
                user_pubkey,
                drift_user_client_manager_object,
                drift_user_account_stats_client_manager,
                drift_strategy_object,
            )
        except Exception as e:
            print(f"Error in UserPortfolio.create: {e}")
            raise e

    def get_user_total_sub_accounts(
        self,
    ) -> int:
        return (
            self.drift_user_account_stats_client_manager.get_account().number_of_sub_accounts
        )

    def get_all_markets(self) -> List:
        return self.drift_user_client_manager_object.get_user_account().perp_positions

    def get_perp_position_market_price(
        self, market_index: int, drift_user_client: DriftUser, market_type: str = "PERP"
    ) -> float:
        match market_type:
            case "PERP":
                return (
                    drift_user_client.get_oracle_data_for_perp_market(
                        market_index
                    ).price
                    / PRICE_PRECISION
                )
            case "SPOT":
                return (
                    drift_user_client.get_oracle_data_for_spot_market(
                        market_index
                    ).price
                    / PRICE_PRECISION
                )

    def get_perp_position_liquidation_price(
        self, market_index: int, drift_user_client: DriftUser
    ) -> float:
        liqudation_price = drift_user_client.get_perp_liq_price(market_index)
        if liqudation_price == -1:
            return 0
        return liqudation_price / PRICE_PRECISION

    def transform_perp_position_values(self, perp_position: PerpPosition):
        update_fields(
            perp_position,
            "quote_entry_amount",
            perp_position.quote_entry_amount / QUOTE_PRECISION,
        )
        update_fields(
            perp_position,
            "quote_break_even_amount",
            perp_position.quote_break_even_amount / QUOTE_PRECISION,
        )
        update_fields(
            perp_position,
            "base_asset_amount",
            perp_position.base_asset_amount / BASE_PRECISION,
        )
        update_fields(
            perp_position,
            "quote_asset_amount",
            perp_position.quote_asset_amount / QUOTE_PRECISION,
        )
        update_fields(
            perp_position,
            "remainder_base_asset_amount",
            perp_position.remainder_base_asset_amount / PRICE_PRECISION,
        )
        update_fields(
            perp_position,
            "last_base_asset_amount_per_lp",
            perp_position.last_base_asset_amount_per_lp / PRICE_PRECISION,
        )
        update_fields(
            perp_position,
            "last_quote_asset_amount_per_lp",
            perp_position.last_quote_asset_amount_per_lp / PRICE_PRECISION,
        )
        update_fields(
            perp_position, "open_bids", perp_position.open_bids / PRICE_PRECISION
        )
        update_fields(
            perp_position, "open_asks", perp_position.open_asks / PRICE_PRECISION
        )
        update_fields(
            perp_position, "settled_pnl", perp_position.settled_pnl / PRICE_PRECISION
        )

    async def get_user_all_perpetual_positions(
        self,
    ) -> Optional[List[CustomPerpPosition]]:
        try:
            if self.current_market_data is None:
                await self.get_current_market_data()
            response = []
            total_sub_accounts = self.get_user_total_sub_accounts()
            if total_sub_accounts is not None and total_sub_accounts > 0:
                for sub_account_id in range(total_sub_accounts):
                    perp_positions = []
                    drift_user_client = await self.drift_user_client_manager_object.get_drift_user_account_client(
                        sub_account_id
                    )
                    if self.current_market_data is None:
                        return None
                    else:
                        for marketIndex in range(
                            len(self.current_market_data.get("perp").keys())
                        ):
                            perp_position = drift_user_client.get_perp_position(
                                marketIndex
                            )
                            if perp_position is None:
                                continue
                            self.transform_perp_position_values(perp_position)
                            data_to_add = {
                                "current_price": self.get_perp_position_market_price(
                                    marketIndex, drift_user_client
                                ),
                                "symbol": self.current_market_data.get("perp").get(
                                    marketIndex
                                ),
                                "liquidation_price": self.get_perp_position_liquidation_price(
                                    marketIndex, drift_user_client
                                ),
                            }
                            perp_position_transformed = (
                                convert_perp_position_to_response_perp_position(
                                    perp_position=perp_position,
                                    data=data_to_add,
                                )
                            )
                            perp_positions.append(perp_position_transformed.__dict__)
                    response.extend(perp_positions)
                filtered_data = filter_fields_for_dataclass(
                    response, CustomPerpPosition
                )
                return filtered_data

        except Exception as e:
            print(f"Error in getting user positions: {e}")
            return None
