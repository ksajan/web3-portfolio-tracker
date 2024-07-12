from types import NoneType

from app.src.clients.drift.clients.drift_client import DriftClientManager
from app.src.clients.web3.factory import Web3ClientFactory
from app.src.clients.zeta.clients.zeta_client import ZetaClientManager
from app.src.loader.constants import async_clients
from app.src.logger.logger import logger


async def subscribe_all_clients():
    try:
        for client_type in async_clients.keys():
            for network_type in async_clients[client_type].keys():
                client = async_clients[client_type][network_type]
                if client is not None:
                    match client_type:
                        case "drift_client":
                            drift_client = client()
                            if drift_client is None:
                                raise ValueError("Error in setting drift client")
                            driftClientManager = DriftClientManager(network_type)
                            try:
                                await driftClientManager.subscribe(drift_client)
                            except Exception as e:
                                raise ValueError(
                                    f"subscription failed for {client_type} {network_type} with error: {e}"
                                )
                            async_clients[client_type][network_type] = drift_client
                            logger.info(f"Subscribed to {client_type} {network_type}")
                            del driftClientManager
                        case "zeta_client":
                            zeta_client = client()
                            zetaClientManger = ZetaClientManager(network_type)
                            try:
                                zeta_client = await zetaClientManger.subscribe(
                                    zeta_client
                                )
                            except Exception as e:
                                raise ValueError(
                                    f"subscription failed for {client_type} {network_type} with error: {e}"
                                )
                            async_clients[client_type][network_type] = zeta_client
                            logger.info(f"Subscribed to {client_type} {network_type}")
                            del zetaClientManger
                        case "helius":
                            helius_web3_connector_object = client()
                            if isinstance(helius_web3_connector_object, NoneType):
                                helius_web3_connector_object = Web3ClientFactory(
                                    client_type, network_type
                                )
                                helius_web3_connector = (
                                    helius_web3_connector_object.subscribe()
                                )
                                async_clients[client_type][
                                    network_type
                                ] = helius_web3_connector
                                logger.info(
                                    f"Subscribed to {client_type} {network_type}"
                                )
                                del helius_web3_connector_object
                        case _:
                            raise ValueError(f"Invalid client type: {client_type}")
    except Exception as e:
        logger.error(f"Error in subscribing to client: {e}", exc_info=True)


async def clear_internal_resources():
    try:
        for client_type in async_clients.keys():
            for network_type in async_clients[client_type].keys():
                client = async_clients[client_type][network_type]
                if client is not None:
                    match client_type:
                        case "drift_client":
                            driftClientManager = DriftClientManager(network_type)
                            try:
                                await driftClientManager.unsubscribe(client)
                            except Exception as e:
                                raise ValueError(
                                    f"unsubscription failed for {client_type} {network_type} with error: {e}"
                                )
                            logger.info(
                                f"Unsubscribed from {client_type} {network_type}"
                            )
                            del driftClientManager
                        case "zeta_client":
                            zetaClientManger = ZetaClientManager(network_type)
                            try:
                                await zetaClientManger.unsubscribe(client)
                            except Exception as e:
                                raise ValueError(
                                    f"unsubscription failed for {client_type} {network_type} with error: {e}"
                                )
                            logger.info(
                                f"Unsubscribed from {client_type} {network_type}"
                            )
                            del zetaClientManger

                        case "helius":
                            web3_client_factory = Web3ClientFactory(
                                client_type, network_type
                            )
                            try:
                                web3_client_factory.unsubscribe(client)
                            except Exception as e:
                                raise ValueError(
                                    f"unsubscription failed for {client_type} {network_type} with error: {e}"
                                )
                        case _:
                            raise ValueError(f"Invalid client type: {client_type}")
    except Exception as e:
        logger.error(f"Error in clearing internal resources: {e}", exc_info=True)
