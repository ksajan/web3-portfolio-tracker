from app.src.drift.clients.drift_client import DriftClientStrategy

mainnet_drift_client = DriftClientStrategy(chain_type="mainnet").get_drift_client()
devnet_drift_client = DriftClientStrategy(chain_type="devnet").get_drift_client()
