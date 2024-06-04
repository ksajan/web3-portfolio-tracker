from fastapi import APIRouter, HTTPException, Request

from app.models.positions import PerpPosition

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


@router.get("/positions", tags=["portfolio"])
async def get_positions(
    request: Request, wallet_address: str
) -> Optional[PerpPosition]:

    return {"positions": []}
