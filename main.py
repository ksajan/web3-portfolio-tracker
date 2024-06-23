from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.src.init.service_init
from app.route import health, portfolio
from app.src.resource_handler.clients import (
    clear_internal_resources,
    subscribe_all_clients,
)


@asynccontextmanager
async def lifecycle(app: FastAPI):
    # At the startup of the application
    await subscribe_all_clients()
    yield
    # At the shutdown of the application
    await clear_internal_resources()


app = FastAPI(debug=True, title="API", description="API", lifespan=lifecycle)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio.router)
app.include_router(health.health_router)
