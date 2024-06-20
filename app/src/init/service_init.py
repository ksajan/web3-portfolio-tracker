from typing import Callable, Optional

from driftpy.drift_client import DriftClient

from app.constants.networks import Networks
from app.src.drift.clients.drift_client import DriftClientManager
from app.src.loader.constants import async_clients


def register_async_clients(client_type: str, network_type: str):
    print(
        f"Registering async client for client type: {client_type} and network type: {network_type}"
    )

    def decorator(fn):
        async_clients[client_type][network_type] = fn
        return fn

    return decorator


@register_async_clients(client_type="drift_client", network_type="mainnet")
def set_drift_mainnet_client() -> Optional[DriftClient]:
    try:
        mainnet_drift_client_object = DriftClientManager(chain_type="mainnet")
        mainnet_drift_client = mainnet_drift_client_object.get_drift_client()
        if mainnet_drift_client is None:
            raise ValueError(
                f"Error in setting drift client for network type: {Networks.SOLANA.networkTypes.SOLANA_MAINNET.value}"
            )
        return mainnet_drift_client
    except Exception as e:
        print(f"Error in setting drift client: {e}")
        return None


@register_async_clients(client_type="drift_client", network_type="devnet")
def set_drift_devnet_client() -> Optional[DriftClient]:
    try:
        devnet_drift_client_object = DriftClientManager(chain_type="devnet")
        devnet_drift_client = devnet_drift_client_object.get_drift_client()
        if devnet_drift_client is None:
            raise ValueError(
                f"Error in setting drift client for network type: {Networks.SOLANA.networkTypes.SOLANA_DEVNET.value}"
            )
        return devnet_drift_client
    except Exception as e:
        print(f"Error in setting drift client: {e}")
        return None
