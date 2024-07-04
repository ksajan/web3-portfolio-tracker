import json
import os
import subprocess
from typing import List, Optional

from solders.pubkey import Pubkey
from zetamarkets_py.client import Client
from zetamarkets_py.risk import AccountRiskSummary
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount

from app.models.client_response_types import (
    CustomPerpPosition,
    CustomUnrealizedPnLPosition,
)
from app.src.clients.zeta.strategy.zeta_user_client import ZetaUserClientManager


class ZetaUserPortfolio:
    async def __init__(
        self, user_pubkey: str, zeta_user_client_manager: ZetaUserClientManager
    ):
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.zeta_user_client_manager = zeta_user_client_manager
        self.account_risk_summary = await self.get_user_risk_summary()
        self.liquidation_price = await self.get_risk_details()

    @classmethod
    def create(cls, user_pubkey: str, zeta_client: Client):
        try:
            zeta_user_client_manager = ZetaUserClientManager(
                user_pubkey=user_pubkey,
                zeta_client=zeta_client,
            )
            return cls(user_pubkey, zeta_user_client_manager)
        except Exception as e:
            print(f"Error creating UserPortfolio: {e}")
            raise e

    async def get_user_cross_margin_account(self) -> CrossMarginAccount:

        marginAccountData = await CrossMarginAccount.fetch(
            conn=self.zeta_user_client_manager.zeta_client.connection,
            address=self.user_pubkey,
            commitment=self.zeta_user_client_manager.zeta_client.commitment,
            program_id=self.zeta_user_client_manager.exchange.program_id,
        )
        print(marginAccountData.to_json())
        return marginAccountData

    async def get_user_risk_summary(self) -> AccountRiskSummary:
        return (
            await self.zeta_user_client_manager.zeta_client.get_account_risk_summary()
        )

    async def get_risk_details(self) -> float:
        # running the typescript code to get the liquidation price
        typescript_file_path = os.path.join(
            os.path.dirname(__file__), "zeta_typescript.ts"
        )
        # Install the required dependencies from package.json
        dependencies_install = subprocess.run(
            ["npm", "install"],
            check=True,
            text=True,
            capture_output=True,
        )
        print(dependencies_install.stdout, dependencies_install.stderr)

        # Compile & Run the TypeScript code to JavaScript
        result = subprocess.run(
            ["npx", "ts-node", typescript_file_path],
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout, result.stderr)

        # Parse and print the output
        output_lines = result.stdout.split("\n")
        liquidation_price = None
        for line in output_lines:
            try:
                if "liquidationPrice" in line:
                    liquidation_price = float(line.split(":")[1].strip())
            except json.JSONDecodeError:
                continue

        print("Risk Data:", liquidation_price)
        return liquidation_price

    async def get_user_perpetual_positions(
        self,
    ) -> Optional[List[CustomPerpPosition]]:
        # fetch the details from the user's margin account and risk details to return the positions with custom CrossMarginPosition objects
        try:
            response = []
            for asset, position in self.account_risk_summary.positions.items():
                if position.size == 0:
                    continue

                response.append(
                    CustomPerpPosition(
                        base_asset_amount=position.size,
                        market_index=asset.to_index(),
                        symbol=asset.__str__(),
                        current_price=self.account_risk_summary.mark_prices.get(asset),
                        liquidation_price=self.liquidation_price,
                        type="perp",
                        chain="Solana",
                        platform="Zeta",
                        comment="Zeta perp position",
                        category="exposure",
                    )
                )
            return response
        except Exception as e:
            print(f"Error getting user positions: {e}")
            return None

    async def get_user_urealized_pnl(
        self,
    ) -> Optional[List[CustomUnrealizedPnLPosition]]:

        return [
            CustomUnrealizedPnLPosition(
                pnl=self.account_risk_summary.unrealized_pnl,
                symbol="USDC",
                market_index=0,
                type="perp",
                chain="Solana",
                platform="Zeta",
                comment="Zeta unrealized pnl position",
                category="both",
            )
        ]
