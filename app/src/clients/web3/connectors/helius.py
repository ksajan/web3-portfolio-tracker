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
from app.src.logger.logger import logger


class TokenBalanceAPI:
    def __init__(self, http_connector: BaseHTTPConnector, chain_type: str, wallet: str):
        self.http_connector = http_connector
        self.chain_type = chain_type
        self.wallet = wallet

    def get_asset_by_owner(self, method: str, url: str) -> RpcResponse[AssetList]:
        try:
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
            print("\n**********\n" + "api response" + "\n**********\n")
            print(
                self.http_connector._make_post_request(
                    url=url,
                    payload=payload.model_dump(
                        mode="json", by_alias=True, exclude_none=True
                    ),
                )
            )
            return RpcResponse[AssetList](
                **self.http_connector._make_post_request(
                    url=url,
                    payload=payload.model_dump(
                        mode="json", by_alias=True, exclude_none=True
                    ),
                )
            )
        except Exception as e:
            logger.error(f"Error in get_asset_by_owner: {e}", exc_info=True)

    def search_assets(
        self,
        method: str,
        url: str,
    ) -> RpcResponse[AssetList]:
        try:
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
            response = self.http_connector._make_post_request(
                url=url,
                payload=payload.model_dump(
                    mode="json",
                    by_alias=True,
                    exclude_none=True,
                ),
            )
            # print("\n**********\n", response, "\n**********\n")
            rpc_response = RpcResponse[AssetList](**response)
            if rpc_response.error is not None:
                raise ValueError(
                    f"search_assets failed with error: {rpc_response.error.message} and code: {rpc_response.error.code}"
                )
            ##TODO: Add pagination support
            return rpc_response
        except Exception as e:
            raise ValueError(str(e)) from e
