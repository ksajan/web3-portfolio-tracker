from fastapi import APIRouter, HTTPException, Request

from app.controller.portfolio import get_all_positions
from app.utils.helper import get_clients_dataclass

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


@router.get("/positions", tags=["portfolio"])
async def get_positions(
    request: Request, wallet_address: str, chain_type: str = "mainnet"
):
    try:
        clients = get_clients_dataclass(chain_type)
        if clients is None:
            raise HTTPException(status_code=500, detail="Clients are not initialized")
        response = await get_all_positions(wallet_address=wallet_address, clients=clients)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
