import uuid

from fastapi import HTTPException

from app.src.loader.constants import async_clients
from app.models.clients import ProtocolClients


def get_drift_client(chain_type: str):
    if chain_type == "mainnet":
        return async_clients.get("drift_client").get(chain_type)
    elif chain_type == "devnet":
        return async_clients.get("drift_client").get(chain_type)
    else:
        raise HTTPException(status_code=400, detail="Invalid chain type")
def get_clients_dataclass(chain_type: str) -> ProtocolClients:
    return ProtocolClients(
        drift_client=async_clients.get("drift_client").get(chain_type),
        zeta_client=async_clients.get("zeta_client").get(chain_type),
    )


def generate_uuid(**kwargs) -> str:
    uuid_string = ""
    uuid_string = "".join([str(value) + "_" for key, value in kwargs.items()])
    return str(uuid.uuid3(uuid.NAMESPACE_URL, uuid_string))
