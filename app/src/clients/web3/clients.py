from pydantic import BaseModel

from app.constants.web3_enums import DAS_API_Method
from app.src.clients.web3.base import BaseHTTPConnector
from app.src.clients.web3.connectors.helius import TokenBalanceAPI
from app.utils.helper import get_endpoints


class Web3Client(BaseModel):
    def __init__(self, wallet: str, rpc_url: str):
        self.wallet = wallet
        self.rpc_url = rpc_url
        self.base_http_connector = BaseHTTPConnector()

    @staticmethod
    def create(wallet: str, chain_type: str):
        rpc_url = get_endpoints(chain_type)
        return Web3Client(wallet, rpc_url)


class HeliusClient(Web3Client):
    def search_assets(self):
        token_balance_api = TokenBalanceAPI(
            self.base_http_connector, self.chain_type, self.wallet
        )
        return token_balance_api.search_assets(
            method=DAS_API_Method.SEARCH_ASSETS.value, url=self.rpc_url
        )

    def get_asset_by_owner(self):
        token_balance_api = TokenBalanceAPI(
            self.base_http_connector, self.chain_type, self.wallet
        )
        return token_balance_api.get_asset_by_owner(
            method=DAS_API_Method.GET_ASSETSBYOWNER.value, url=self.rpc_url
        )
