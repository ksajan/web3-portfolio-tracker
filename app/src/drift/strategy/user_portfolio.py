from typing import List, Optional

from driftpy.drift_client import DriftClient
from driftpy.drift_user import DriftUser
from driftpy.drift_user_stats import DriftUserStats

from app.models.positions import PerpPosition
from app.src.drift.clients.user_client import (
    DriftUserAccountStatsClientManager,
    DriftUserClientManager,
)


class UserPortfolio:
    def __init__(
        self,
        user_pubkey: str,
        drift_user_client_manager_object: DriftUserClientManager,
        drift_user_account_stats_client_manager: DriftUserStats,
    ):
        self.user_pubkey = user_pubkey
        self.drift_user_client_manager_object = drift_user_client_manager_object
        self.drift_user_account_stats_client_manager = (
            drift_user_account_stats_client_manager
        )

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
            return cls(
                user_pubkey,
                drift_user_client_manager_object,
                drift_user_account_stats_client_manager,
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
        return self.drift_user_client_manager.get_user_account().perp_positions

    async def get_user_all_perpetual_positions(self):
        try:
            response = {}
            for sub_account_id in range(self.get_user_total_sub_accounts()):
                perp_positions = []
                drift_user_client = await self.drift_user_client_manager_object.get_drift_user_account_client(
                    sub_account_id
                )
                for marketIndex in range(30):
                    perp_position = drift_user_client.get_perp_position(marketIndex)
                    if perp_position is None:
                        continue
                    perp_positions.append(perp_position)
                response[sub_account_id] = perp_positions
            return response
        except Exception as e:
            print(f"Error in getting user positions: {e}")
            return None
