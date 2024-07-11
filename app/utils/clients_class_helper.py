from app.models.clients import ProtocolClients
from app.src.loader.constants import async_clients


def get_clients_dataclass(chain_type: str) -> ProtocolClients:
    return ProtocolClients(
        drift_client=async_clients.get("drift_client").get(chain_type),
        zeta_client=async_clients.get("zeta_client").get(chain_type),
        helius_client=async_clients.get("helius").get(chain_type),
    )
