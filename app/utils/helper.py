import uuid

from fastapi import HTTPException

from app.src.loader.constants import async_clients


def get_drift_client(chain_type: str):
    if chain_type == "mainnet":
        return async_clients.get("drift_client").get(chain_type)
    elif chain_type == "devnet":
        return async_clients.get("drift_client").get(chain_type)
    else:
        raise HTTPException(status_code=400, detail="Invalid chain type")


def generate_uuid(**kwargs) -> str:
    uuid_string = ""
    uuid_string = "".join([str(value) + "_" for key, value in kwargs.items()])
    return str(uuid.uuid3(uuid.NAMESPACE_URL, uuid_string))
