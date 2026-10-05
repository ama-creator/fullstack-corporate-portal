from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department


class DepartmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, department_id: int) -> Department | None:
        result = await self.session.execute(
            select(Department).where(Department.id == department_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Department]:
        result = await self.session.execute(
            select(Department).order_by(Department.name)
        )

        return list(result.scalars().all())

    async def get_by_name(
        self,
        name: str,
    ) -> Department | None:
        result = await self.session.execute(
            select(Department).where(func.lower(Department.name) == name.lower())
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        department: Department,
    ) -> Department:
        self.session.add(department)

        await self.session.commit()
        await self.session.refresh(department)

        return department

    async def update(
        self,
        department: Department,
        data: dict[str, object],
    ) -> Department:
        for field, value in data.items():
            setattr(department, field, value)

        await self.session.commit()
        await self.session.refresh(department)

        return department
