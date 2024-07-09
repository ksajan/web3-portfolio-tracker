from driftpy.constants.numeric_constants import PRICE_PRECISION
from driftpy.drift_client import DriftClient
from driftpy.drift_user import BASE_PRECISION, QUOTE_PRECISION, DriftUser
from driftpy.drift_user_stats import DriftUserStats
from driftpy.types import PerpPosition, SpotPosition

from app.constants.common import Symbols
from app.constants.drift_constants import (
    DriftPositionComment,
    DriftPositionType,
    DriftUserPortfolioCategory,
)
from app.models.client_response_types import (
    CustomPerpPosition,
    CustomSpotPosition,
    CustomUnrealizedPnLPosition,
)
from app.src.clients.drift.clients.user_client import (
    DriftUserAccountStatsClientManager,
    DriftUserClientManager,
)
from app.src.clients.drift.strategy.drift_strategy import DriftStrategy
from app.src.clients.drift.utils.helper import (
    convert_perp_position_to_response_perp_position,
    convert_spot_position_to_custom_spot_position,
    filter_fields_for_pydantic_model,
    update_fields,
)
from app.src.logger.logger import logger


class DriftUserPortfolio:
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
            logger.error(f"Error in UserPortfolio.create: {e}", exc_info=True)
            raise e

    def get_user_total_sub_accounts(
        self,
    ) -> int:
        return (
            self.drift_user_account_stats_client_manager.get_account().number_of_sub_accounts
        )

    def get_all_markets(self) -> list:
        return self.drift_user_client_manager_object.get_user_account().perp_positions

    def get_market_price(
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

    def get_position_liquidation_price(
        self, market_index: int, drift_user_client: DriftUser, market_type: str = "PERP"
    ) -> float:
        match market_type:
            case "PERP":
                liqudation_price = drift_user_client.get_perp_liq_price(market_index)
                if (
                    liqudation_price == -1
                    or liqudation_price == 0
                    or liqudation_price is None
                ):
                    return 0
                return liqudation_price / PRICE_PRECISION
            case "SPOT":
                liqudation_price = drift_user_client.get_spot_liq_price(market_index)
                if (
                    liqudation_price == -1
                    or liqudation_price == 0
                    or liqudation_price is None
                ):
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

    async def get_user_perpetual_positions(
        self,
    ) -> list[CustomPerpPosition] | None:
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
                            data_to_add = {
                                "current_price": self.get_market_price(
                                    marketIndex, drift_user_client, "PERP"
                                ),
                                "symbol": self.current_market_data.get("perp").get(
                                    marketIndex
                                ),
                                "liquidation_price": self.get_position_liquidation_price(
                                    marketIndex, drift_user_client, "PERP"
                                ),
                                "category": DriftUserPortfolioCategory.EXPOSURE_CATEGORY.value,
                                "comment": DriftPositionComment.PERP.value,
                            }
                            self.transform_perp_position_values(perp_position)
                            perp_position_transformed = (
                                convert_perp_position_to_response_perp_position(
                                    perp_position=perp_position,
                                    data=data_to_add,
                                )
                            )
                            perp_positions.append(perp_position_transformed.__dict__)
                    response.extend(perp_positions)
                filtered_data = filter_fields_for_pydantic_model(
                    response, CustomPerpPosition
                )
                if filtered_data is None:
                    raise Exception("Error in filtering fields for dataclass")
                return filtered_data

        except Exception as e:
            logger.error(f"Error in getting user positions: {e}", exc_info=True)
            return None

    def transform_spot_position_values(self, spot_position: SpotPosition):
        update_fields(
            spot_position,
            "scaled_balance",
            spot_position.scaled_balance / BASE_PRECISION,
        )
        update_fields(
            spot_position,
            "cumulative_deposits",
            spot_position.cumulative_deposits / BASE_PRECISION,
        )
        update_fields(
            spot_position, "open_bids", spot_position.open_bids / BASE_PRECISION
        )
        update_fields(
            spot_position, "open_asks", spot_position.open_asks / BASE_PRECISION
        )

    async def get_user_spot_positions(self) -> list[CustomSpotPosition] | None:
        try:
            if self.current_market_data is None:
                await self.get_current_market_data()
            response = []
            total_sub_accounts = self.get_user_total_sub_accounts()
            if total_sub_accounts is not None and total_sub_accounts > 0:
                for sub_account_id in range(total_sub_accounts):
                    spot_positions = []
                    drift_user_client = await self.drift_user_client_manager_object.get_drift_user_account_client(
                        sub_account_id
                    )
                    if self.current_market_data is None or drift_user_client is None:
                        return None
                    else:
                        for marketIndex in range(
                            len(self.current_market_data.get("spot").keys())
                        ):
                            spot_position = drift_user_client.get_spot_position(
                                marketIndex
                            )
                            if spot_position is None:
                                continue
                            data_to_add = {
                                "current_price": self.get_market_price(
                                    marketIndex, drift_user_client, "SPOT"
                                ),
                                "symbol": self.current_market_data.get("spot").get(
                                    marketIndex
                                ),
                                "liquidation_price": self.get_position_liquidation_price(
                                    marketIndex, drift_user_client, "SPOT"
                                ),
                                "category": DriftUserPortfolioCategory.EXPOSURE_CATEGORY.value,
                                "comment": DriftPositionComment.SPOT.value,
                            }
                            self.transform_spot_position_values(spot_position)
                            spot_position = (
                                convert_spot_position_to_custom_spot_position(
                                    spot_position=spot_position,
                                    data=data_to_add,
                                )
                            )
                            spot_positions.append(spot_position.__dict__)

                    response.extend(spot_positions)
                filtered_data = filter_fields_for_pydantic_model(
                    response, CustomSpotPosition
                )
                if filtered_data is None:
                    raise Exception("Error in filtering fields for dataclass")
                return filtered_data

        except Exception as e:
            logger.error(f"Error in getting user positions: {e}", exc_info=True)
            return None

    async def get_user_unrealized_pnl(
        self,
    ) -> list[CustomUnrealizedPnLPosition] | None:
        try:
            if self.current_market_data is None:
                await self.get_current_market_data()
            response = []
            total_sub_accounts = self.get_user_total_sub_accounts()
            if total_sub_accounts is not None and total_sub_accounts > 0:
                for sub_account_id in range(total_sub_accounts):
                    unrealized_pnl = 0
                    drift_user_client = await self.drift_user_client_manager_object.get_drift_user_account_client(
                        sub_account_id
                    )
                    if drift_user_client is None or self.current_market_data is None:
                        continue
                    else:
                        for marketIndex in range(
                            len(self.current_market_data.get("perp").keys())
                        ):
                            unrealized_pnl = drift_user_client.get_unrealized_pnl(
                                market_index=marketIndex
                            )
                            if unrealized_pnl is None or unrealized_pnl == 0:
                                continue
                            custom_unrealized_pnl = CustomUnrealizedPnLPosition(
                                pnl=unrealized_pnl / PRICE_PRECISION,
                                symbol=Symbols.UDSC.value,
                                type=DriftPositionType.SPOT_TYPE.value,  ## All unrealized pnl is spot type
                                market_index=marketIndex,
                                category=DriftUserPortfolioCategory.BOTH_CATEGORY.value,
                                comment=f"Drift UPnL on {self.current_market_data.get('perp').get(marketIndex)}",
                            )
                            response.append(custom_unrealized_pnl.__dict__)
                        for marketIndex in range(
                            len(self.current_market_data.get("spot").keys())
                        ):
                            unrealized_pnl = drift_user_client.get_unrealized_pnl(
                                market_index=marketIndex
                            )
                            if unrealized_pnl is None or unrealized_pnl == 0:
                                continue
                            custom_unrealized_pnl = CustomUnrealizedPnLPosition(
                                pnl=unrealized_pnl / PRICE_PRECISION,
                                symbol=Symbols.UDSC.value,
                                type=DriftPositionType.SPOT_TYPE.value,
                                market_index=marketIndex,
                                category=DriftUserPortfolioCategory.BOTH_CATEGORY.value,
                                comment=f"Drift UPnL on {self.current_market_data.get('spot').get(marketIndex)}",
                            )
                            response.append(custom_unrealized_pnl.__dict__)
                filtered_data = filter_fields_for_pydantic_model(
                    response, CustomUnrealizedPnLPosition
                )
                return filtered_data
        except Exception as e:
            logger.error(f"Error in getting unrealized pnl: {e}", exc_info=True)
            return None
