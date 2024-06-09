from driftpy.account_subscription_config import AccountSubscriptionConfig
from driftpy.accounts.bulk_account_loader import BulkAccountLoader
from driftpy.addresses import (
    get_user_account_public_key,
    get_user_stats_account_public_key,
)
from driftpy.drift_client import DriftClient
from driftpy.drift_user import DriftUser
from driftpy.drift_user_stats import DriftUserStats, UserStatsSubscriptionConfig
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # type: ignore


class DriftUserClientManager:
    def __init__(self, user_pubkey: str, drift_client: DriftClient):
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.drift_client = drift_client

    def get_user_account_pubkey(self, sub_account_id: int = 0) -> Pubkey:
        return get_user_account_public_key(
            program_id=self.drift_client.program_id,
            authority=self.user_pubkey,
            sub_account_id=sub_account_id,
        )

    def get_bulk_account_loader(self, connection: AsyncClient):
        return BulkAccountLoader(connection)

    def get_account_subscription_config(
        self, connection: AsyncClient
    ) -> AccountSubscriptionConfig:
        return AccountSubscriptionConfig(
            type="polling", bulk_account_loader=self.get_bulk_account_loader(connection)
        )

    async def get_drift_user_account_client(self, sub_account_id: int = 0) -> DriftUser:
        driftUser = DriftUser(
            self.drift_client,
            self.get_user_account_pubkey(sub_account_id=sub_account_id),
            self.get_account_subscription_config(self.drift_client.connection),
        )
        await driftUser.subscribe()
        return driftUser


class DriftUserAccountStatsClientManager:
    def __init__(self, user_pubkey: str, drift_client: DriftClient):
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.drift_client = drift_client

    def get_user_stats_account_pubkey(self) -> Pubkey:
        return get_user_stats_account_public_key(
            program_id=self.drift_client.program_id, authority=self.user_pubkey
        )

    def get_user_stats_subscription_config(self) -> UserStatsSubscriptionConfig:
        return UserStatsSubscriptionConfig(
            commitment="confirmed",
        )

    async def get_user_stats_account_client(
        self,
    ) -> DriftUserStats:
        driftUserStats = DriftUserStats(
            self.drift_client,
            self.get_user_stats_account_pubkey(),
            self.get_user_stats_subscription_config(),
        )
        await driftUserStats.subscribe()
        return driftUserStats
