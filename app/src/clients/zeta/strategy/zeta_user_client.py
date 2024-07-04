from solders.pubkey import Pubkey
from zetamarkets_py import pda
from zetamarkets_py.client import Client


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
