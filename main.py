import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.route import portfolio
from app.src.init.service_init import init_drift_clients

app = FastAPI(debug=True, title="API", description="API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Quant Portfolio API Service"}


@app.get("/health")
def health_check():
    return {"status": True, "message": "Service is up and running"}


@app.on_event("startup")
async def startup_event():
    await init_drift_clients(app)


app.include_router(portfolio.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8002)
