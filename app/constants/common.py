from enum import Enum
from typing import Literal

DriftEnv = Literal["devnet", "mainnet"]


class Symbols(Enum):
    UDSC = "UDSC"
