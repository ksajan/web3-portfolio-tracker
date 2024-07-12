from app.src.logger.logger import logger

from .clients import HeliusClient, Web3Client


class Web3ClientFactory:
    def __init__(self, client_type: str, chain_type: str):
        self.client_type = client_type
        self.chain_type = chain_type

    def get_web3_client_connector(self) -> Web3Client | None:
        try:
            return None  # Web3Client.create(self.chain_type, self.client_type)
        except Exception as e:
            logger.error(f"Error getting Zeta client: {e}", exc_info=True)
            return None

    def subscribe(self) -> HeliusClient | None:
        try:
            return Web3Client.create(self.chain_type, self.client_type)
        except Exception as e:
            logger.error(f"Error in setting web3 client: {e}", exc_info=True)
            return None

    def unsubscribe(self, client: HeliusClient | None) -> None:
        if client is None:
            return
        del client
        logger.info(f"Unsubscribed from {self.client_type} {self.chain_type}")
