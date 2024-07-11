from app.src.clients.web3.base import BaseHTTPConnector
from app.src.clients.web3.connectors.types.enums import TokenType
from app.src.clients.web3.connectors.types.options import (
    DisplayOptions,
    SearchAssetsOptions,
)
from app.src.clients.web3.connectors.types.types import (
    AssetList,
    GetAssetsByOwner,
    RpcRequest,
    RpcResponse,
    SearchAssets,
)


class TokenBalanceAPI:
    def __init__(self, http_connector: BaseHTTPConnector, chain_type: str, wallet: str):
        self.http_connector = http_connector
        self.chain_type = chain_type
        self.wallet = wallet

    def get_asset_by_owner(self, method: str, url: str) -> RpcResponse[AssetList]:
        if len(url) == 0:
            raise ValueError(f"RPC URL is empty for chain type: {self.chain_type}")
        payload = RpcRequest.new(
            method=method,
            parameters=GetAssetsByOwner(
                owner_address=self.wallet,
                page=1,
                limit=10,
                display_options=DisplayOptions(
                    showNativeBalance=True,
                ),
            ),
        )
        return self.http_connector._make_post_request(url=url, payload=payload)

    def search_assets(
        self,
        method: str,
        url: str,
    ) -> RpcResponse[AssetList]:
        if len(url) == 0:
            raise ValueError(f"RPC URL is empty for chain type: {self.chain_type}")
        payload = RpcRequest.new(
            method=method,
            parameters=SearchAssets(
                owner_address=self.wallet,
                token_type=TokenType.fungible,
                displayOptions=SearchAssetsOptions(
                    showNativeBalance=True,
                ),
            ),
        )
        return self.http_connector._make_post_request(url=url, payload=payload)
