from fastapi import APIRouter

health_router = APIRouter(tags=["health"])


@health_router.get("/")
def read_root():
    return {"message": "Welcome to Quant Portfolio API Service"}


@health_router.get("/health")
def health_check():
    return {"status": True, "message": "Service is up and running"}
