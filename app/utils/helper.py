import uuid

import app.src.loader.env_vars as _env_vars

SOLANA_MAINNET_RPC = _env_vars.SOLANA_MAINNET_RPC_URL
SOLANA_DEVNET_RPC = _env_vars.SOLANA_DEVNET_RPC_URL


def generate_uuid(**kwargs) -> str:
    uuid_string = ""
    uuid_string = "".join([str(value) + "_" for key, value in kwargs.items()])
    return str(uuid.uuid3(uuid.NAMESPACE_URL, uuid_string))


def generate_random_id() -> str:
    return str(uuid.uuid4())


def get_endpoints(chain_type: str) -> str | None:
    match chain_type:
        case "solana":
            return SOLANA_MAINNET_RPC
        case "solana_dev":
            return SOLANA_DEVNET_RPC
        case _:
            return None
