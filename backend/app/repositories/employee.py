from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, limit: int, offset: int) -> list[Employee]:
        result = await self.session.execute(
            select(Employee).order_by(Employee.id).limit(limit).offset(offset)
        )

        return result.scalars().all()

    async def get_by_id(self, employee_id: int) -> Employee | None:
        result = await self.session.execute(
            select(Employee).where(Employee.id == employee_id)
        )

        return result.scalar_one_or_none()
