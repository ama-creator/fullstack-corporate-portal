from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.repositories.employee import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self.repository = repository

    async def get_all(
        self,
        limit: int,
        offset: int,
        department_id: int | None = None,
        position_id: int | None = None,
        role: EmployeeRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Employee], int]:
        employees = await self.repository.get_all(
            limit=limit,
            offset=offset,
            department_id=department_id,
            position_id=position_id,
            role=role,
            is_active=is_active,
            search=search,
        )

        total = await self.repository.count(
            department_id=department_id,
            position_id=position_id,
            role=role,
            is_active=is_active,
            search=search,
        )
        
        return employees, total

    async def get_by_id(self, employee_id: int) -> Employee | None:
        return await self.repository.get_by_id(employee_id)
