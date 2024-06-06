import os

from dotenv import find_dotenv, load_dotenv

if find_dotenv():
    print(
        "Found .env file.",
    )
    load_dotenv(find_dotenv())

SOLANA_MAINNET_RPC_URL = os.getenv("SOLANA_MAINNET_RPC_URL")
SOLANA_DEVNET_RPC_URL = os.getenv("SOLANA_DEVNET_RPC_URL")
