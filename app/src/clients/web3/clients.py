from typing import Optional

from pydantic import BaseModel

from app.constants.web3_enums import DAS_API_Method
from app.models.client_response_types import CustomOnChainPosition
from app.src.clients.web3.base import BaseHTTPConnector
from app.src.clients.web3.connectors.helius import TokenBalanceAPI
from app.src.logger.logger import logger
from app.utils.helper import get_endpoints


class Web3Client(BaseModel):
    rpc_url: str
    chain_type: str
    base_http_connector: Optional[BaseHTTPConnector] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.base_http_connector = BaseHTTPConnector()

    @staticmethod
    def create(chain_type: str, client_type: str):
        rpc_url = get_endpoints(chain_type)
        match client_type:
            case "helius":
                return HeliusClient(rpc_url=rpc_url, chain_type=chain_type)
            # case "test":
            #     return TestClient(rpc_url=rpc_url, chain_type=chain_type)
            case _:
                raise ValueError(f"Chain type: {chain_type} not supported")


class HeliusClient(Web3Client):
    def __init__(self, **data):
        super().__init__(**data)

    def get_onchain_positions(self, wallet: str) -> list[CustomOnChainPosition] | None:
        try:
            token_balance_api = TokenBalanceAPI(
                self.base_http_connector, self.chain_type, wallet
            )
            response_data = token_balance_api.search_assets(
                method=DAS_API_Method.SEARCH_ASSETS.value, url=self.rpc_url
            )
            if response_data.error:
                raise ValueError(response_data.error.message)
            onchain_positions = []
            for asset in response_data.result.items:
                if (
                    asset.token_info is not None
                    and asset.token_info.price_info is not None
                ):
                    onchain_position = CustomOnChainPosition(
                        symbol=asset.token_info.symbol,
                        amount=asset.token_info.balance,
                        current_price=asset.token_info.price_info.price_per_token,
                        total_price=asset.token_info.price_info.total_price,
                        chain="Solana",
                        platform="Solana",
                        type="spot",
                        category="both",
                        comment="Solana on-chain position",
                        side="long",
                        liquidation_price=0.0,  # Constant value in case of onchain positions
                    )
                    onchain_positions.append(onchain_position)
            return onchain_positions
        except Exception as e:
            logger.error(
                f"error fetching onchain positions: {str(e)}",
                exc_info=True,
                extra={"wallet": wallet, "client_type": "HeliusClient"},
            )
            return None

    def get_onchain_positions_by_owner(self, wallet: str) -> dict:
        token_balance_api = TokenBalanceAPI(
            self.base_http_connector, self.chain_type, wallet
        )
        return token_balance_api.get_asset_by_owner(
            method=DAS_API_Method.GET_ASSETSBYOWNER.value, url=self.rpc_url
        )
