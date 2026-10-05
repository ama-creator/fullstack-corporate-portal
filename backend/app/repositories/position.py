from sqlalchemy import func, select
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

    async def get_all(self) -> list[Position]:
        result = await self.session.execute(select(Position).order_by(Position.name))

        return list(result.scalars().all())

    async def get_by_name(
        self,
        name: str,
    ) -> Position | None:
        result = await self.session.execute(
            select(Position).where(func.lower(Position.name) == name.lower())
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        position: Position,
    ) -> Position:
        self.session.add(position)

        await self.session.commit()
        await self.session.refresh(position)

        return position

    async def update(
        self,
        position: Position,
        data: dict[str, object],
    ) -> Position:
        for field, value in data.items():
            setattr(position, field, value)

        await self.session.commit()
        await self.session.refresh(position)

        return position
