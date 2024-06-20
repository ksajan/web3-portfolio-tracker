from fastapi import APIRouter, HTTPException, Request

from app.controller.portfolio import get_all_positions
from app.utils.helper import get_drift_client

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


@router.get("/positions", tags=["portfolio"])
async def get_positions(
    request: Request, wallet_address: str, chain_type: str = "mainnet"
):
    try:
        drift_client = get_drift_client(request.app, chain_type)
        if drift_client is None:
            raise HTTPException(
                status_code=500, detail="Drift client is not initialized"
            )
        response = await get_all_positions(wallet_address, drift_client)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
