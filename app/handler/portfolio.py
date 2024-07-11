import asyncio

from fastapi import HTTPException

from app.constants.error import ClientPositionError
from app.handler.position import PositionFactory
from app.models.client_response_types import (
    CustomPerpPosition,
    CustomSpotPosition,
    CustomUnrealizedPnLPosition,
)
from app.models.clients import ProtocolClients
from app.models.response_positions import (
    ResponsePerpPosition,
    ResponsePositionBase,
    ResponseSpotPosition,
    ResponseUnrealizedPnLPosition,
)
from app.src.clients.drift.strategy.user_portfolio import DriftUserPortfolio
from app.src.clients.web3.clients import Web3Client
from app.src.clients.zeta.strategy.user_portfolio import ZetaUserPortfolio
from app.src.logger.logger import logger


class Positions:
    def __init__(self, wallet_address: str, clients: ProtocolClients):
        self.positions = []
        self.wallet_address = wallet_address
        self.drift_client = clients.drift_client
        self.zeta_client = clients.zeta_client

    async def initialize_user_portfolio(self):
        if self.drift_client is None:
            raise HTTPException(
                status_code=500, detail="Drift client is not initialized"
            )
        self.user_portfolio = await DriftUserPortfolio.create(
            self.wallet_address, self.drift_client
        )
        if self.zeta_client is None:
            raise HTTPException(
                status_code=500, detail="Zeta client is not initialized"
            )
        self.zeta_user_portfolio: ZetaUserPortfolio = ZetaUserPortfolio.create(
            self.wallet_address, self.zeta_client
        )
        self.on_chain_portfolio = Web3Client.create(
            self.wallet_address,
        )

    def get_perp_markets(self):
        perp_markets = self.user_portfolio.get_all_markets()
        return perp_markets

    def _populate_response_perp_positions(
        self, perp_positions: list[CustomPerpPosition]
    ) -> list[ResponsePerpPosition]:
        try:
            response_perp_positions = []
            for perp_position in perp_positions:
                response_perp_position = PositionFactory.create_response_perp_position(
                    perp_position, self.wallet_address
                )
                response_perp_positions.append(response_perp_position)
            return response_perp_positions
        except Exception as e:
            logger.error(
                f"Error in populating response perp positions: {e}", exc_info=True
            )
            return []

    async def get_perp_positions(
        self, client, error_enum
    ) -> list[tuple[list[ResponsePerpPosition], list[str]]]:
        try:
            perp_positions = await client.get_user_perpetual_positions()
            if perp_positions is None:
                return [
                    [],
                    [(error_enum.PERP_POSITION_NOT_FOUND.value)],
                ]
            response = self._populate_response_perp_positions(perp_positions)
            return [response, []]
        except Exception as e:
            logger.error(f"Error in getting perp positions: {e}", exc_info=True)
            return [[], [(error_enum.PERP_POSITION_NOT_FOUND.value)]]

    async def get_all_perp_positions(
        self,
    ) -> tuple[list[ResponsePerpPosition], list[str]]:
        try:
            drift_future = self.get_perp_positions(
                self.user_portfolio, ClientPositionError.DRIFT_POSITION_ERROR.value
            )
            zeta_future = self.get_perp_positions(
                self.zeta_user_portfolio, ClientPositionError.ZETA_POSITION_ERROR.value
            )
            drift_response, zeta_response = await asyncio.gather(
                drift_future, zeta_future
            )
            return (
                drift_response[0] + zeta_response[0],
                drift_response[1] + zeta_response[1],
            )
        except Exception as e:
            logger.error(f"Error in getting all perp positions: {e}", exc_info=True)
            return [], [
                ClientPositionError.GENERAL_POSITION_ERROR.value.PERP_POSITION_NOT_FOUND
            ]

    def _populate_response_spot_positions(
        self, spot_positions: list[CustomSpotPosition]
    ) -> list[ResponseSpotPosition]:
        try:
            response_spot_positions = []
            for spot_position in spot_positions:
                response_spot_position = PositionFactory.create_response_spot_position(
                    spot_position, self.wallet_address
                )
                response_spot_positions.append(response_spot_position)
            return response_spot_positions
        except Exception as e:
            logger.error(
                f"Error in populating response spot positions: {e}", exc_info=True
            )
            return []

    async def get_spot_positions(
        self, client, error_enum
    ) -> list[tuple[list[ResponseSpotPosition], list[str]]]:
        try:
            spot_positions = await client.get_user_spot_positions()
            if spot_positions is None:
                return [
                    [],
                    [(error_enum.SPOT_POSITION_NOT_FOUND.value)],
                ]  # [ClientPositionError(error_enum.SPOT_POSITION_NOT_FOUND)]
            response = self._populate_response_spot_positions(spot_positions)
            return [response, []]
        except Exception as e:
            logger.error(f"Error in getting spot positions: {e}", exc_info=True)
            return [[], [(error_enum.SPOT_POSITION_NOT_FOUND.value)]]

    async def get_all_spot_positions(
        self,
    ) -> tuple[list[ResponseSpotPosition], list[str]]:
        try:
            drift_spot_future = self.get_spot_positions(
                self.user_portfolio, ClientPositionError.DRIFT_POSITION_ERROR.value
            )
            zeta_spot_future = self.get_spot_positions(
                self.zeta_user_portfolio, ClientPositionError.ZETA_POSITION_ERROR.value
            )
            drift_response, zeta_response = await asyncio.gather(
                drift_spot_future, zeta_spot_future
            )
            return (
                drift_response[0] + zeta_response[0],
                drift_response[1] + zeta_response[1],
            )
        except Exception as e:
            logger.error(f"Error in getting all spot positions: {e}", exc_info=True)
            return [], [
                ClientPositionError.GENERAL_POSITION_ERROR.value.SPOT_POSITION_NOT_FOUND
            ]

    def _populate_unrealized_pnl_positions(
        self, unrealized_pnl_positions: list[CustomUnrealizedPnLPosition]
    ) -> list[ResponseUnrealizedPnLPosition]:
        try:
            response_unrealized_pnl_positions = []
            for unrealized_pnl_position in unrealized_pnl_positions:
                response_unrealized_pnl_position = (
                    PositionFactory.create_response_unrealized_pnl_position(
                        unrealized_pnl_position, self.wallet_address
                    )
                )
                response_unrealized_pnl_positions.append(
                    response_unrealized_pnl_position
                )
            return response_unrealized_pnl_positions
        except Exception as e:
            logger.error(
                f"Error in populating response unrealized pnl positions: {e}",
                exc_info=True,
            )
            return []

    async def get_unrealized_pnl_positions(
        self, client, error_enum
    ) -> list[tuple[list[ResponseUnrealizedPnLPosition], list[str]]]:
        try:
            unrealized_pnl_positions = await client.get_user_unrealized_pnl()
            if unrealized_pnl_positions is None:
                return [
                    [],
                    [(error_enum.UNREALIZED_PNL_POSITION_NOT_FOUND.value)],
                ]
            response = self._populate_unrealized_pnl_positions(unrealized_pnl_positions)
            return [response, []]
        except Exception as e:
            logger.error(
                f"Error in getting unrealized pnl positions: {e}", exc_info=True
            )
            return [
                [],
                [(error_enum.UNREALIZED_PNL_POSITION_NOT_FOUND.value)],
            ]

    async def get_all_unrealized_pnl_positions(
        self,
    ) -> tuple[list[ResponseUnrealizedPnLPosition], list[str]]:
        try:
            drift_unrealized_pnl_future = self.get_unrealized_pnl_positions(
                self.user_portfolio, ClientPositionError.DRIFT_POSITION_ERROR.value
            )
            zeta_unrealized_pnl_future = self.get_unrealized_pnl_positions(
                self.zeta_user_portfolio, ClientPositionError.ZETA_POSITION_ERROR.value
            )
            drift_response, zeta_response = await asyncio.gather(
                drift_unrealized_pnl_future, zeta_unrealized_pnl_future
            )
            return (
                drift_response[0] + zeta_response[0],
                drift_response[1] + zeta_response[1],
            )
        except Exception as e:
            logger.error(
                f"Error in getting all unrealized pnl positions: {e}", exc_info=True
            )
            return [], [
                ClientPositionError.GENERAL_POSITION_ERROR.value.UPNL_POSITION_NOT_FOUND.value
            ]

    def filter_small_positions(
        self,
        positions: list[ResponsePositionBase],
    ) -> list[
        set[ResponsePerpPosition, ResponseSpotPosition, ResponseUnrealizedPnLPosition]
    ]:
        try:
            for position in positions:
                if position.notional_usd < 1 and position.margin_usd < 1:
                    positions.remove(position)
            return positions
        except Exception as e:
            logger.error(f"Error in filtering small positions: {e}", exc_info=True)
            return positions

    ## FIXME: Fix this function where when used with asyncio.gather to call all the functions concurrently, it creates new resources such running the typescript twice which increases the time by 3~5 seconds
    # async def get_all_positions(self) -> dict[str, list[dict[str, any]]]:
    #     try:
    #         await self.initialize_user_portfolio()

    #         # Run the tasks concurrently
    #         perp_task = self.get_all_perp_positions()
    #         spot_task = self.get_all_spot_positions()
    #         upnl_task = self.get_all_unrealized_pnl_positions()

    #         results = await asyncio.gather(
    #             perp_task, spot_task, upnl_task, return_exceptions=True
    #         )

    #         perp_positions, perp_errors = results[0]
    #         spot_positions, spot_error = results[1]
    #         unrealized_pnl_positions, upnl_errors = results[2]

    #         filtered_all_positions = self.filter_small_positions(
    #             positions=perp_positions + spot_positions + unrealized_pnl_positions
    #         )

    #         return {
    #             "positions": filtered_all_positions,
    #             "errors": perp_errors + spot_error + upnl_errors,
    #         }

    #     except Exception as e:
    #         logger.error(
    #             f"Error in getting positions for wallet: {self.wallet_address} with error: {e}",
    #             exc_info=True,
    #         )
    #         return {
    #             "positions": [],
    #             "errors": [ClientPositionError.GENERAL_POSITION_ERROR],
    #         }
    async def get_all_positions(
        self,
    ) -> dict[str, list[ResponsePositionBase]]:
        try:
            await self.initialize_user_portfolio()
            perp_positions, perp_errors = await self.get_all_perp_positions()
            spot_positions, spot_error = await self.get_all_spot_positions()
            unrealized_pnl_positions, upnl_errors = (
                await self.get_all_unrealized_pnl_positions()
            )
            filtered_all_positions = self.filter_small_positions(
                positions=perp_positions + spot_positions + unrealized_pnl_positions
            )
            return {
                "positions": filtered_all_positions,
                "errors": perp_errors + spot_error + upnl_errors,
            }
        except Exception as e:
            logger.error(
                f"Error in getting positions for wallet: {self.wallet_address} with error: {e}",
                exc_info=True,
            )
            return {
                "positions": [],
                "errors": [ClientPositionError.GENERAL_POSITION_ERROR.value],
            }
