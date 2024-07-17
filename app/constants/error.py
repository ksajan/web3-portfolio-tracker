from enum import Enum


class ClientError(Enum):
    DRIFT_CLIENT_NOT_INITIALIZED = "Drift client is not initialized"
    ZETA_CLIENT_NOT_INITIALIZED = "Zeta client is not initialized"


class DriftPositionError(Enum):
    PERP_POSITION_NOT_FOUND = "Drift perp position not found"
    SPOT_POSITION_NOT_FOUND = "Drift spot position not found"
    UPNL_POSITION_NOT_FOUND = "Drift upnl position not found"


class ZetaPositionError(Enum):
    PERP_POSITION_NOT_FOUND = "Zeta perp position not found"
    SPOT_POSITION_NOT_FOUND = "Zeta spot position not found"
    UPNL_POSITION_NOT_FOUND = "Zeta upnl position not found"


class GenralPositionError(Enum):
    PERP_POSITION_NOT_FOUND = "Perp position not found"
    SPOT_POSITION_NOT_FOUND = "Spot position not found"
    UPNL_POSITION_NOT_FOUND = "Upnl position not found"


class ClientPositionError(Enum):
    DRIFT_POSITION_ERROR = DriftPositionError
    ZETA_POSITION_ERROR = ZetaPositionError
    GENERAL_POSITION_ERROR = GenralPositionError
