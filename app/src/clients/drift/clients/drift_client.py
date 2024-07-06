from typing import Optional

from anchorpy import Wallet
from driftpy.drift_client import DriftClient
from driftpy.keypair import load_keypair
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair  # type: ignore

import app.src.loader.env_vars as env_vars
from app.constants.common import DriftEnv
from app.constants.networks import Networks
from app.src.logger.logger import logger

SOLANA_DEVNET_RPC_URL = env_vars.SOLANA_DEVNET_RPC_URL
SOLANA_MAINNET_RPC_URL = env_vars.SOLANA_MAINNET_RPC_URL


class DriftClientEnvChainType:
    DEVNET = "devnet"
    MAINNET = "mainnet"


class DriftClientManager:
    def __init__(self, chain_type: DriftEnv):
        self.chain_type = chain_type
        self.network_constants = Networks.SOLANA
        self.validate_chain_type()

    def validate_chain_type(self) -> None:
        if self.chain_type not in [
            DriftClientEnvChainType.DEVNET,
            DriftClientEnvChainType.MAINNET,
        ]:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    def get_user_keypair(self, private_key: str) -> Keypair:
        """Get a keypair from a private key file, generally a .json file."""
        return load_keypair(private_key)

    def get_user_wallet_from_keypair(self, keypair: Keypair) -> Wallet:
        return Wallet(keypair)

    def get_dummy_wallet(self) -> Wallet:
        return Wallet.dummy()

    def get_rpc_connection_client(self) -> AsyncClient:
        try:
            if (
                self.chain_type
                == self.network_constants.networkTypes.SOLANA_MAINNET.value
            ):
                return AsyncClient(endpoint=SOLANA_MAINNET_RPC_URL)
            elif (
                self.chain_type
                == self.network_constants.networkTypes.SOLANA_DEVNET.value
            ):
                print("Using devnet", SOLANA_DEVNET_RPC_URL)
                return AsyncClient(endpoint=SOLANA_DEVNET_RPC_URL)
            else:
                raise ValueError(
                    f"Invalid chain type for drift client: {self.chain_type}"
                )
        except Exception as e:
            raise ValueError(f"Error in getting rpc connection client: {e}")

    def get_drift_client(self) -> Optional[DriftClient]:
        try:
            connection = self.get_rpc_connection_client()
            wallet = self.get_dummy_wallet()
            drift_client = DriftClient(
                connection=connection,
                wallet=wallet,
                env=self.chain_type,
            )
            return drift_client
        except Exception as e:
            logger.error(f"Error in getting drift client: {e}")
            return None

    async def subscribe(self, drift_client: DriftClient) -> None:
        try:
            await drift_client.subscribe()
        except Exception as e:
            raise ValueError(f"Error: {e}")

    async def unsubscribe(self, drift_client: DriftClient) -> None:
        try:
            await drift_client.unsubscribe()
        except Exception as e:
            raise ValueError(f"Error: {e}")
