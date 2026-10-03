from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position import Position


class PositionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, position_id: int) -> Position | None:
        result = await self.session.execute(
            select(Position).where(Position.id == position_id)
        )

        return result.scalar_one_or_none()
