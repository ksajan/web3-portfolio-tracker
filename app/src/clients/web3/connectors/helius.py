from app.src.clients.web3.base import BaseHTTPConnector


class BalanceAPI(BaseHTTPConnector):
    def get_balance(self) -> dict:
        url = self.get_endpoints()
        if url is None:
            raise ValueError(f"Invalid chain type: {self.chain_type}")
        url += "/balance/" + self.wallet
        return self._make_get_request(url)


class TokenBalanceAPI(BaseHTTPConnector):
    def get_asset_by_owner(self) -> dict:
        url = self.get_endpoints()
        if url is None:
            raise ValueError(f"Invalid chain type: {self.chain_type}")
        # payload = json.dumps(
        #     {
        #         "jsonrpc": "2.0",
        #         "id": "my-id",
        #         "method": "searchAssets",
        #         "params": {
        #             "ownerAddress": "BvDMnDXHxw8dLTyfMJWwsZVWsAGzYfJrUak1W3uJ76R4",
        #             "tokenType": "fungible",
        #             "displayOptions": {"showNativeBalance": True},
        #         },
        #     }
        # )
        payload = 
