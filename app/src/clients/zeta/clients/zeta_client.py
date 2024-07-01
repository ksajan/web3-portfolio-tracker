import anchorpy
from anchorpy import Wallet
from zetamarkets_py.client import Client

from app.constants.networks import Networks


class ZetaClient(Client):
    def __init__(self, chain_type: str):
        super().__init__(chain_type)
        self.chain_type = chain_type
        self.network_constants = Networks.SOLANA
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

    def get_rpc_connection_client(self) -> 
