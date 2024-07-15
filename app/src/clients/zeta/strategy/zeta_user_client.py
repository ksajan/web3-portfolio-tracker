import anchorpy
from solders.pubkey import Pubkey
from zetamarkets_py import pda
from zetamarkets_py.client import Client
from zetamarkets_py.risk import AccountRiskSummary
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zetamarkets_py.zeta_client.accounts.pricing import Pricing

from app.src.logger.logger import logger


class ZetaUserClientManager:
    def __init__(self, user_pubkey: str, zeta_client: Client):
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.zeta_client = zeta_client

        """
                    key = wallet.public_key if delegator_pubkey is None else delegator_pubkey

                    _margin_account_manager_address = pda.get_cross_margin_account_manager_address(exchange.program_id, key)
                    _user_usdc_address = pda.get_associated_token_address(key, constants.USDC_MINT[network])
                    _margin_account_address = pda.get_margin_account_address(exchange.program_id, key, 0)
                    margin_account = await CrossMarginAccount.fetch(
                        connection, _margin_account_address, connection.commitment, exchange.program_id
                    )
        """

    def get_user_margin_account_address(self, sub_account_id: int = 0) -> Pubkey:
        return pda.get_margin_account_address(
            self.zeta_client.exchange.program_id, self.user_pubkey, sub_account_id
        )

    async def get_user_risk_summary(self) -> AccountRiskSummary:
        try:
            account_infos = await anchorpy.utils.rpc.get_multiple_accounts(
                self.zeta_client.connection,
                [
                    self.get_user_margin_account_address(),
                    self.zeta_client.exchange._pricing_address,
                ],
            )
            if (
                account_infos is None
                or account_infos[0] is None
                or account_infos[0].account is None
                or len(account_infos) < 2
            ):
                return None
            margin_account = CrossMarginAccount.decode(account_infos[0].account.data)
            pricing_account = Pricing.decode(account_infos[1].account.data)
            accountRiskSummary = AccountRiskSummary.from_margin_and_pricing_accounts(
                margin_account, pricing_account
            )
            return accountRiskSummary
        except Exception as e:
            logger.error(f"Error getting user risk summary: {e}", exc_info=True)
            return None
