from typing import Any, Dict, List

from fastapi import HTTPException

from app.src.drift.strategy.user_portfolio import UserPortfolio
from app.src.init.service_init import devnet_drift_client, mainnet_drift_client


async def user_positions(chain_type: str, wallet_address: str) -> List[Dict[str, Any]]:
    print(chain_type, "chain type sajan controller")
    drift_client = (
        mainnet_drift_client if chain_type == "mainnet" else devnet_drift_client
    )
    if drift_client is None:
        raise HTTPException(status_code=500, detail="Drift client is not initialized")
    print(drift_client.program_id, "hello program id sajan controller")
    user_portfolio = await UserPortfolio.create(wallet_address, drift_client)
    return user_portfolio.get_user_all_perpetual_positions(
        user_portfolio.drift_user_client_manager
    )
