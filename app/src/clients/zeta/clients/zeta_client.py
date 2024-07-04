import anchorpy
from anchorpy import Wallet
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from zetamarkets_py.client import Client
from zetamarkets_py.exchange import Exchange
from zetamarkets_py.types import Asset, Network

import app.src.loader.env_vars as env_vars
from app.constants.networks import Networks

SOLANA_DEVNET_RPC_URL = env_vars.SOLANA_DEVNET_RPC_URL
SOLANA_MAINNET_RPC_URL = env_vars.SOLANA_MAINNET_RPC_URL


class ZetaClient(Client):
    def __init__(self, chain_type: str):
        super().__init__(chain_type)
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

    def get_user_wallet_from_keypair(self, keypair: anchorpy.Keypair) -> Wallet:
        return Wallet(keypair)

    def get_dummy_wallet(self) -> Wallet:
        return Wallet.dummy()

    def get_rpc_connection_client(self) -> AsyncClient:
        if self.chain_type == self.network_constants.networkTypes.SOLANA_MAINNET.value:
            return AsyncClient(endpoint=SOLANA_MAINNET_RPC_URL)
        elif self.chain_type == self.network_constants.networkTypes.SOLANA_DEVNET.value:
            return AsyncClient(endpoint=SOLANA_DEVNET_RPC_URL)
        else:
            raise ValueError(f"Invalid chain type for drift client: {self.chain_type}")

    async def get_zeta_client(self) -> Client:
        try:
            zeta_client = await Client.load(
                endpoint=self.rpc_url,
                network=(
                    Network.MAINNET
                    if self.chain_type
                    == self.network_constants.networkTypes.SOLANA_MAINNET.value
                    else Network.DEVNET
                ),
            )
            # zeta_client.get_account_risk_summary()
            return zeta_client
        except Exception as e:
            print(f"Error getting Zeta client: {e}")
            return None

    async def get_zeta_exchange_client(self) -> Exchange:
        try:
            connection = AsyncClient(endpoint=self.rpc_url, commitment=Confirmed)
            exchange = await Exchange.load(
                network=self.network,
                connection=connection,
                assets=Asset.all(),
            )
            return exchange
        except Exception as e:
            print(f"Error getting Zeta exchange client: {e}")
            return None
