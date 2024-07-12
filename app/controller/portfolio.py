from fastapi import HTTPException

from app.handler.portfolio import Positions
from app.models.clients import ProtocolClients


async def get_all_positions(
    wallet_address: str, clients: ProtocolClients
) -> dict[str, list]:
    try:
        position_object = Positions(wallet_address=wallet_address, clients=clients)
        all_positions = await position_object.get_all_positions()
        if all_positions is None:
            raise HTTPException(status_code=404, detail="No positions found")
        return all_positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in getting positions: {e}")
