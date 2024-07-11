from .clients import HeliusClient, Web3Client


class Web3ClientFactory:
    def __init__(self, client_type: str, chain_type: str):
        self.client_type = client_type
        self.chain_type = chain_type

    def get_web3_client_connector(self, wallet: str) -> Web3Client:
        match self.client_type:
            case "helius":
                return HeliusClient.create(wallet=wallet, chain_type=self.chain_type)
            case _:
                raise ValueError(f"Client type: {self.client_type} not supported")

    def subscribe(self):
        pass
