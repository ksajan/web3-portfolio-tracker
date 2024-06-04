from anchorpy import Wallet
from driftpy.account_subscription_config import AccountSubscriptionConfig
from driftpy.accounts.bulk_account_loader import BulkAccountLoader
from driftpy.addresses import (
    get_user_account_public_key,
    get_user_stats_account_public_key,
)
from driftpy.drift_client import DriftClient
from driftpy.drift_user import DriftUser
from driftpy.keypair import load_keypair
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey


class DriftClient:
    def __init__(self, chain_type):
        self.chain_type = chain_type

    def get_user_keypair(self, private_key: str) -> Keypair:
        """Get a keypair from a private key file, generally a .json file."""
        return load_keypair(private_key)

    def get_user_wallet_from_keypair(self, keypair: Keypair) -> Wallet:
        return Wallet(keypair)

    def get_dummy_wallet(self) -> Wallet:
        return Wallet.dummy()

    def get_rpc_connection_client(self) -> AsyncClient:
        

    def get_drift_client(self):
        return
