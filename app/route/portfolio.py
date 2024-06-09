from typing import List, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Request

from app.models.positions import PerpPosition
from app.src.drift.strategy.user_portfolio import UserPortfolio

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


def get_drift_client(app: FastAPI, chain_type: str):
    if chain_type == "mainnet":
        return app.state.mainnet_drift_client
    elif chain_type == "devnet":
        return app.state.devnet_drift_client
    else:
        raise HTTPException(status_code=400, detail="Invalid chain type")


@router.get("/positions", tags=["portfolio"])
async def get_positions(request: Request, wallet_address: str, chain_type: str):
    try:
        drift_client = get_drift_client(request.app, chain_type)
        if drift_client is None:
            raise HTTPException(
                status_code=500, detail="Drift client is not initialized"
            )
        user_portfolio = await UserPortfolio.create(wallet_address, drift_client)
        return await user_portfolio.get_user_all_perpetual_positions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
