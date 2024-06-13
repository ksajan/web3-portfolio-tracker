from typing import Any, Dict, List

from driftpy.drift_client import DriftClient
from fastapi import HTTPException

from app.handler.portfolio import Positions


async def get_all_positions(
    wallet_address: str, drift_client: DriftClient
) -> List[Dict[str, Any]]:
    try:
        position_object = Positions(
            wallet_address=wallet_address, drift_client=drift_client
        )
        await position_object.initialize_user_portfolio()
        all_positions = await position_object.get_all_positions()
        if all_positions is None:
            raise HTTPException(status_code=404, detail="No positions found")
        return all_positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in getting positions: {e}")
