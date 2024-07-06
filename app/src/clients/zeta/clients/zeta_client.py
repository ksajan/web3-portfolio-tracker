from typing import Optional

import anchorpy
from anchorpy import Wallet
from solana.rpc.async_api import AsyncClient
from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, Network

import app.src.loader.env_vars as env_vars
from app.constants.networks import Networks
from app.src.logger.logger import logger

SOLANA_DEVNET_RPC_URL = env_vars.SOLANA_DEVNET_RPC_URL
SOLANA_MAINNET_RPC_URL = env_vars.SOLANA_MAINNET_RPC_URL


class ZetaClientManager:
    def __init__(self, chain_type: str):
        self.chain_type = chain_type
        self.network_constants = Networks.SOLANA
        self.network = (
            Network.MAINNET
            if self.chain_type
            == self.network_constants.networkTypes.SOLANA_MAINNET.value
            else Network.DEVNET
        )
        self.rpc_url = (
            SOLANA_MAINNET_RPC_URL
            if self.chain_type
            == self.network_constants.networkTypes.SOLANA_MAINNET.value
            else SOLANA_DEVNET_RPC_URL
        )
        self.validate_chain_type()

    def validate_chain_type(self) -> None:
        if self.chain_type not in [
            self.network_constants.networkTypes.SOLANA_MAINNET.value,
            self.network_constants.networkTypes.SOLANA_DEVNET.value,
        ]:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    def get_dummy_wallet(self) -> Wallet:
        return Wallet.dummy()

    def get_rpc_connection_client(self) -> AsyncClient:
        if self.chain_type == self.network_constants.networkTypes.SOLANA_MAINNET.value:
            return AsyncClient(endpoint=SOLANA_MAINNET_RPC_URL)
        elif self.chain_type == self.network_constants.networkTypes.SOLANA_DEVNET.value:
            return AsyncClient(endpoint=SOLANA_DEVNET_RPC_URL)
        else:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    def get_zeta_client(self) -> Optional[Client]:
        try:
            # zeta_client.get_account_risk_summary()
            return None
        except Exception as e:
            logger.error(f"Error getting Zeta client: {e}")
            return None

    async def subscribe(self, zeta_client: Optional[Client]) -> Client:
        try:
            if zeta_client is not None:
                return await zeta_client.load(
                    endpoint=self.rpc_url,
                    network=(
                        Network.MAINNET
                        if self.chain_type
                        == self.network_constants.networkTypes.SOLANA_MAINNET.value
                        else Network.DEVNET
                    ),
                )
            else:
                return await Client.load(
                    endpoint=self.rpc_url,
                    network=(
                        Network.MAINNET
                        if self.chain_type
                        == self.network_constants.networkTypes.SOLANA_MAINNET.value
                        else Network.DEVNET
                    ),
                )
        except Exception as e:
            raise ValueError(f"Error: {e}")

    async def unsubscribe(self, zeta_client: Client) -> None:
        try:
            del zeta_client
            pass
        except Exception as e:
            raise ValueError(f"Error: {e}")
