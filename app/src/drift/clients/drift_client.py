from anchorpy import Wallet
from driftpy.drift_client import DriftClient
from driftpy.keypair import load_keypair
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair  # type: ignore

from app.constants.common import DriftEnv
from app.constants.networks import NetworkConstants
from app.src.loader.env_vars import SOLANA_DEVNET_RPC_URL, SOLANA_MAINNET_RPC_URL


class DriftClientStrategy:
    def __init__(self, chain_type):
        self.chain_type = chain_type
        self.network_constants = NetworkConstants()
        self.validate_chain_type()

    def validate_chain_type(self) -> None:
        if self.chain_type not in DriftEnv:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    def get_user_keypair(self, private_key: str) -> Keypair:
        """Get a keypair from a private key file, generally a .json file."""
        return load_keypair(private_key)

    def get_user_wallet_from_keypair(self, keypair: Keypair) -> Wallet:
        return Wallet(keypair)

    def get_dummy_wallet(self) -> Wallet:
        return Wallet.dummy()

    def get_rpc_connection_client(self) -> AsyncClient:
        if self.chain_type == self.network_constants.SOLANA_MAINNET:
            return AsyncClient(endpoint=SOLANA_MAINNET_RPC_URL)
        elif self.chain_type == self.network_constants.SOLANA_DEVNET:
            return AsyncClient(endpoint=SOLANA_DEVNET_RPC_URL)
        else:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    async def get_drift_client(self) -> DriftClient:
        try:
            drift_client = DriftClient(
                connection=self.get_rpc_connection_client(),
                wallet=self.get_dummy_wallet(),
                env=self.chain_type,
            )
            await drift_client.subscribe()
            print("Subscribed to drift client")
            return drift_client
        except Exception as e:
            print(f"Error in getting drift client: {e}")
            return None
