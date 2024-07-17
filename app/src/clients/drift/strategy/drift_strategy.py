from driftpy.drift_client import DriftClient


class DriftStrategy:
    def __init__(self, drift_client: DriftClient) -> None:
        self.drift_client = drift_client

    async def get_markets(self) -> dict[str, dict]:
        all_markets = {"perp": {}, "spot": {}}
        all_perp_markets = await self.drift_client.program.account["PerpMarket"].all()
        sorted_perp_markets = sorted(
            all_perp_markets, key=lambda x: x.account.market_index
        )
        for market in sorted_perp_markets:
            all_markets["perp"][market.account.market_index] = (
                bytes(market.account.name).decode("utf-8").strip()
            )

        all_spot_markets = await self.drift_client.program.account["SpotMarket"].all()
        sorted_spot_markets = sorted(
            all_spot_markets, key=lambda x: x.account.market_index
        )
        for market in sorted_spot_markets:
            all_markets["spot"][market.account.market_index] = (
                bytes(market.account.name).decode("utf-8").strip()
            )

        return all_markets
