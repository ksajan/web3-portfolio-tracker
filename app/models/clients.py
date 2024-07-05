from dataclasses import dataclass

from driftpy.drift_client import DriftClient
from pydantic import BaseModel
from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset


@dataclass
class ProtocolClients:
    drift_client: DriftClient
    zeta_client: Client


class LiquidationPrice(BaseModel):
    market_index: int
    liquidation_price: float
    asset: Asset
