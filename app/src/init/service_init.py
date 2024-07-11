from driftpy.drift_client import DriftClient
from zetamarkets_py.client import Client

# import app.src.loader.env_vars
from app.constants.networks import Networks
from app.src.clients.drift.clients.drift_client import DriftClientManager
from app.src.clients.web3.factory import Web3ClientFactory
from app.src.clients.zeta.clients.zeta_client import ZetaClientManager
from app.src.loader.constants import async_clients
from app.src.logger.logger import logger


def register_async_clients(client_type: str, network_type: str, skip: bool = False):
    def decorator(fn):
        if not skip:
            async_clients[client_type][network_type] = fn
        return fn

    return decorator


@register_async_clients(client_type="drift_client", network_type="mainnet")
def set_drift_mainnet_client() -> DriftClient | None:
    try:
        mainnet_drift_client_object = DriftClientManager(chain_type="mainnet")
        mainnet_drift_client = mainnet_drift_client_object.get_drift_client()
        if mainnet_drift_client is None:
            raise ValueError(
                f"Error in setting drift client for network type: {Networks.SOLANA.networkTypes.SOLANA_MAINNET.value}"
            )
        return mainnet_drift_client
    except Exception as e:
        logger.error(f"Error in setting drift client: {e}", exc_info=True)
        return None


@register_async_clients(client_type="drift_client", network_type="devnet", skip=True)
def set_drift_devnet_client() -> DriftClient | None:
    try:
        devnet_drift_client_object = DriftClientManager(chain_type="devnet")
        devnet_drift_client = devnet_drift_client_object.get_drift_client()
        if devnet_drift_client is None:
            raise ValueError(
                f"Error in setting drift client for network type: {Networks.SOLANA.networkTypes.SOLANA_DEVNET.value}"
            )
        return devnet_drift_client
    except Exception as e:
        logger.error(f"Error in setting drift client: {e}", exc_info=True)
        return None


@register_async_clients(client_type="zeta_client", network_type="mainnet")
def set_zeta_mainnet_client() -> Client | None:
    try:
        mainnet_zeta_client_object = ZetaClientManager(chain_type="mainnet")
        mainnet_zeta_client = mainnet_zeta_client_object.get_zeta_client()
        return mainnet_zeta_client
    except Exception as e:
        logger.error(f"Error in setting zeta client: {e}", exc_info=True)
        return None


@register_async_clients(client_type="zeta_client", network_type="devnet", skip=True)
def set_zeta_devnet_client() -> Client | None:
    try:
        devnet_zeta_client_object = ZetaClientManager(chain_type="devnet")
        devnet_zeta_client = devnet_zeta_client_object.get_zeta_client()
        return devnet_zeta_client
    except Exception as e:
        logger.error(f"Error in setting zeta client: {e}", exc_info=True)
        return None


@register_async_clients(client_type="helius", network_type="mainnet")
def set_web3_mainnet_client() -> Web3ClientFactory | None:
    try:
        mainnet_web3_client = Web3ClientFactory(
            client_type="helius", chain_type="mainnet"
        )
        return mainnet_web3_client
    except Exception as e:
        logger.error(f"Error in setting web3 client: {e}", exc_info=True)
        return None
