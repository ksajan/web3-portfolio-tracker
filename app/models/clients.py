from dataclasses import dataclass

from driftpy.drift_client import DriftClient
from zetamarkets_py.client import Client


@dataclass
class ProtocolClients:
    drift_client: DriftClient
    zeta_client: Client
