from typing import Any, Dict, List

from driftpy.drift_client import DriftClient
from fastapi import HTTPException

from app.src.drift.strategy.user_portfolio import UserPortfolio
from app.src.init.service_init import devnet_drift_client, mainnet_drift_client


async def get_all_positions(
    wallet_address: str, drift_client: DriftClient
) -> List[Dict[str, Any]]:
    # user_portfolio = await UserPortfolio.create(wallet_address, drift_client)
    # return user_portfolio.get_user_all_perpetual_positions(
    #     user_portfolio.drift_user_client_manager
    # )
    pass
