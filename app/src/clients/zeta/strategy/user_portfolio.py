import json
import os
import subprocess
import traceback
from typing import List, Optional

import anchorpy
from solders.pubkey import Pubkey
from zetamarkets_py.client import Client
from zetamarkets_py.risk import AccountRiskSummary
from zetamarkets_py.types import Asset
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zetamarkets_py.zeta_client.accounts.pricing import Pricing

from app.models.client_response_types import (
    CustomPerpPosition,
    CustomUnrealizedPnLPosition,
)
from app.models.clients import LiquidationPrice
from app.src.clients.zeta.strategy.zeta_user_client import ZetaUserClientManager
from app.src.loader import env_vars

SOLANA_MAINNET_RPC = env_vars.SOLANA_MAINNET_RPC_URL
SOLANA_DEVNET_RPC = env_vars.SOLANA_DEVNET_RPC_URL


class ZetaUserPortfolio:
    def __init__(
        self, user_pubkey: str, zeta_user_client_manager: ZetaUserClientManager
    ):
        self.liquidation_price = None
        self.account_risk_summary = None
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.zeta_user_client_manager = zeta_user_client_manager

    async def init_zeta_resource(self):
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
            commitment=self.zeta_user_client_manager.zeta_client.connection.commitment,
            program_id=self.zeta_user_client_manager.zeta_client.exchange.program_id,
        )
        print(marginAccountData.to_json())
        return marginAccountData

    async def get_user_risk_summary(self) -> AccountRiskSummary:
        try:
            account_infos = await anchorpy.utils.rpc.get_multiple_accounts(
                self.zeta_user_client_manager.zeta_client.connection,
                [
                    self.zeta_user_client_manager.get_user_margin_account_address(),
                    self.zeta_user_client_manager.zeta_client.exchange._pricing_address,
                ],
            )
            margin_account = CrossMarginAccount.decode(account_infos[0].account.data)
            pricing_account = Pricing.decode(account_infos[1].account.data)
            accountRiskSummary = AccountRiskSummary.from_margin_and_pricing_accounts(
                margin_account, pricing_account
            )
            return accountRiskSummary
        except Exception as e:
            print(f"Error getting user risk summary: {e}")
            traceback.print_exc()
            return None

    async def get_risk_details(self) -> Optional[List[LiquidationPrice]]:
        try:
            # running the typescript code to get the liquidation price
            typescript_file_path = os.path.join(
                os.path.dirname(__file__), "zeta_typescript.ts"
            )

            # Compile & Run the TypeScript code to JavaScript
            result = subprocess.run(
                [
                    "npx",
                    "ts-node",
                    typescript_file_path,
                    "--endpoint",
                    self.zeta_user_client_manager.zeta_client.endpoint,
                    "--network",
                    self.zeta_user_client_manager.zeta_client.network.__str__().lower(),
                    "--user_pubkey",
                    self.user_pubkey.__str__(),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            # Parse and print the output
            output_lines = result.stdout.split("\n")
            response = []
            for line in output_lines:
                try:
                    if "Asset" in line:
                        values = line.split(",")
                        _ = values[0].split(":")[1].strip()
                        index = int(values[1].split(":")[1].strip())
                        liquidation_price = float(values[2].split(":")[1].strip())
                        response.append(
                            LiquidationPrice(
                                market_index=index,
                                liquidation_price=liquidation_price,
                                asset=Asset.from_index(index),
                            )
                        )
                except json.JSONDecodeError:
                    continue

            print("Risk Data:", response)
            return response
        except Exception as e:
            print(f"Error getting risk details: {e}")
            traceback.print_exc()
            return None

    async def get_user_perpetual_positions(
        self,
    ) -> Optional[List[CustomPerpPosition]]:
        try:
            await self.init_zeta_resource()
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
                        liquidation_price=self.liquidation_price[
                            asset.to_index()
                        ].liquidation_price,
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

    async def get_user_unrealized_pnl(
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
