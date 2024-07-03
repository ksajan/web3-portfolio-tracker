from solders.pubkey import Pubkey
from zetamarkets_py.client import Client
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount

from app.src.clients.zeta.strategy.zeta_user_client import ZetaUserClientManager


class UserPortfolio:
    def __init__(
        self, user_pubkey: str, zeta_user_client_manager: ZetaUserClientManager
    ):
        self.user_pubkey = Pubkey.from_string(user_pubkey)
        self.zeta_user_client_manager = zeta_user_client_manager

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

    async def get_risk_details(self):
        # running the typescript code to get the liquidation price
        pass

    async def get_user_positions(self):
        # fetch the details from the user's margin account and risk details to return the positions with custom CrossMarginPosition objects
        # return the positions
        pass
