from enum import Enum


class Networks(Enum):
    SOLANA = "solana"

    @property
    def networkTypes(self):
        match self:
            case Networks.SOLANA:
                return SolanaNetworkTypes
            case _:
                raise ValueError("Invalid network type")


class SolanaNetworkTypes(Enum):
    SOLANA_MAINNET = "mainnet"
    SOLANA_DEVNET = "devnet"
