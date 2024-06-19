import asyncio

from app.src.drift.clients.drift_client import DriftClientManager
from app.src.loader.constants import async_clients


def register_async_clients():
    async_clients["mainnet"] = None
    async_clients["devnet"] = None


async def set_drift_client():
    mainnet_drift_client_object = DriftClientManager(chain_type="mainnet")
    mainnet_drift_client = mainnet_drift_client_object.get_drift_client()
    await mainnet_drift_client.subscribe()

    devnet_drift_client_object = DriftClientManager(chain_type="devnet")
    devnet_drift_client = devnet_drift_client_object.get_drift_client()
    await devnet_drift_client.subscribe()
    return mainnet_drift_client, devnet_drift_client


async def init_drift_clients(app):
    mainnet_drift_client, devnet_drift_client = await set_drift_client()
    app.state.mainnet_drift_client = mainnet_drift_client
    app.state.devnet_drift_client = devnet_drift_client
