from fastapi import FastAPI
from app.api.v1.routers.wallet import router as router_wallet

app=FastAPI(
    title="Wallet Service API",
    description="Cервис для управления кошельками",
    version="1.0.0"
)

app.include_router(router_wallet, prefix="/api/v1", tags=["wallets"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}