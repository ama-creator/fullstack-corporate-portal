from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self.repository = repository

    async def get_all(self, limit: int, offset: int) -> list[Employee]:
        return await self.repository.get_all(limit=limit, offset=offset)

    async def get_by_id(self, employee_id: int) -> Employee | None:
        return await self.repository.get_by_id(employee_id)