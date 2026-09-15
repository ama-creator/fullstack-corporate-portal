from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/db")
async def database_health_check(
    session: DbSession,
) -> dict[str, int]:
    result = await session.execute(text("SELECT 1"))
    value = result.scalar_one()

    return {"database": value}
