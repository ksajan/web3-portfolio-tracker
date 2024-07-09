from app.src.clients.web3.base import BaseHTTPConnector
from app.src.clients.web3.connectors.types.types import (
    AssetList,
    GetAssetsByOwner,
    SearchAssets,
)


class BalanceAPI(BaseHTTPConnector):
    def get_balance(self) -> dict:
        url = self.get_endpoints()
        if url is None:
            raise ValueError(f"Invalid chain type: {self.chain_type}")
        url += "/balance/" + self.wallet
        return self._make_get_request(url)


class TokenBalanceAPI(BaseHTTPConnector):
    def get_asset_by_owner(self, payload: GetAssetsByOwner) -> AssetList:
        url = self.get_endpoints()
        if url is None:
            raise ValueError(f"Invalid chain type: {self.chain_type}")
        return self._make_post_request(url=url, payload=payload)

    def search_assets(self, payload: SearchAssets) -> AssetList:
        url = self.get_endpoints()
        if url is None:
            raise ValueError(f"Invalid chain type: {self.chain_type}")
        return self._make_post_request(url=url, payload=payload)
