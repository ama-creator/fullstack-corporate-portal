from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router

app = FastAPI(
    title="Corporate Portal API",
    description="Production-like corporate portal backend",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
