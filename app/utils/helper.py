import uuid

from fastapi import FastAPI, HTTPException


def get_drift_client(app: FastAPI, chain_type: str):
    if chain_type == "mainnet":
        return app.state.mainnet_drift_client
    elif chain_type == "devnet":
        return app.state.devnet_drift_client
    else:
        raise HTTPException(status_code=400, detail="Invalid chain type")


def generate_uuid(**kwargs) -> str:
    uuid_string = ""
    uuid_string = "".join([str(value) + "_" for key, value in kwargs.items()])
    return str(uuid.uuid3(uuid.NAMESPACE_URL, uuid_string))
