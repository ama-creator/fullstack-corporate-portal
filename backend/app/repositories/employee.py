from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.models.enums import EmployeeRole


class EmployeeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(
        self,
        limit: int,
        offset: int,
        department_id: int | None = None,
        position_id: int | None = None,
        role: EmployeeRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> list[Employee]:
        query = select(Employee)

        query = self._apply_filters(
            query=query,
            department_id=department_id,
            position_id=position_id,
            role=role,
            is_active=is_active,
            search=search,
        )

        query = query.order_by(Employee.id).limit(limit).offset(offset)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_by_id(self, employee_id: int) -> Employee | None:
        result = await self.session.execute(
            select(Employee).where(Employee.id == employee_id)
        )

        return result.scalar_one_or_none()

    def _apply_filters(
        self,
        query,
        department_id: int | None = None,
        position_id: int | None = None,
        role: EmployeeRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ):
        if department_id is not None:
            query = query.where(Employee.department_id == department_id)

        if position_id is not None:
            query = query.where(Employee.position_id == position_id)

        if role is not None:
            query = query.where(Employee.role == role)

        if is_active is not None:
            query = query.where(Employee.is_active == is_active)

        if search is not None:
            search_pattern = f"%{search}%"

            query = query.where(
                Employee.first_name.ilike(search_pattern)
                | Employee.last_name.ilike(search_pattern)
                | Employee.middle_name.ilike(search_pattern)
                | Employee.email.ilike(search_pattern)
            )

        return query

    async def count(
        self,
        department_id: int | None = None,
        position_id: int | None = None,
        role: EmployeeRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> int:
        query = select(func.count()).select_from(Employee)

        query = self._apply_filters(
            query=query,
            department_id=department_id,
            position_id=position_id,
            role=role,
            is_active=is_active,
            search=search,
        )

        result = await self.session.execute(query)

        return result.scalar_one()

    async def get_by_email(self, email: str) -> Employee | None:
        result = await self.session.execute(
            select(Employee).where(Employee.email == email)
        )

        return result.scalar_one_or_none()

    async def create(self, employee: Employee) -> Employee:
        self.session.add(employee)

        await self.session.commit()
        await self.session.refresh(employee)

        return employee
    
    async def update(
        self,
        employee: Employee,
        data: dict[str, object],
    ) -> Employee:
        for field, value in data.items():
            setattr(employee, field, value)
    
        await self.session.commit()
        await self.session.refresh(employee)
    
        return employee