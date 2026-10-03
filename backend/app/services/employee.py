from app.core.security import hash_password
from app.exceptions import (
    DepartmentNotFoundError,
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    PermissionDeniedError,
    PositionNotFoundError,
    SelfModificationError,
)
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.repositories.position import PositionRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(
        self,
        repository: EmployeeRepository,
        department_repository: DepartmentRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.repository = repository
        self.department_repository = department_repository
        self.position_repository = position_repository

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

    async def create(
        self,
        data: EmployeeCreate,
        actor: Employee,
    ) -> Employee:
        existing_employee = await self.repository.get_by_email(str(data.email))

        if existing_employee is not None:
            raise EmployeeAlreadyExistsError

        if data.department_id is not None:
            department = await self.department_repository.get_by_id(data.department_id)

            if department is None:
                raise DepartmentNotFoundError

        if data.position_id is not None:
            position = await self.position_repository.get_by_id(data.position_id)

            if position is None:
                raise PositionNotFoundError

        if actor.role == EmployeeRole.HR and data.role in {
            EmployeeRole.ADMIN,
            EmployeeRole.HR,
        }:
            raise PermissionDeniedError

        employee = Employee(
            email=str(data.email),
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            phone=data.phone,
            birth_date=data.birth_date,
            hire_date=data.hire_date,
            department_id=data.department_id,
            position_id=data.position_id,
            role=data.role,
            is_active=True,
        )

        return await self.repository.create(employee)

    async def update(
        self,
        employee_id: int,
        data: EmployeeUpdate,
        actor: Employee,
    ) -> Employee:
        employee = await self.repository.get_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError

        # Can actor modify this employee?
        if actor.role == EmployeeRole.HR and employee.role in {
            EmployeeRole.ADMIN,
            EmployeeRole.HR,
        }:
            raise PermissionDeniedError

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return employee

        if actor.id == employee.id and actor.role == EmployeeRole.ADMIN:
            new_role = update_data.get("role")
            new_is_active = update_data.get("is_active")

            if new_role is not None and new_role != EmployeeRole.ADMIN:
                raise SelfModificationError

            if new_is_active is False:
                raise SelfModificationError

        # Validate department.
        if "department_id" in update_data:
            department_id = update_data["department_id"]

            if department_id is not None:
                department = await self.department_repository.get_by_id(department_id)

                if department is None:
                    raise DepartmentNotFoundError

        # Validate position.
        if "position_id" in update_data:
            position_id = update_data["position_id"]

            if position_id is not None:
                position = await self.position_repository.get_by_id(position_id)

                if position is None:
                    raise PositionNotFoundError

        # Can actor assign this role?
        if "role" in update_data:
            new_role = update_data["role"]

            if actor.role == EmployeeRole.HR and new_role in {
                EmployeeRole.ADMIN,
                EmployeeRole.HR,
            }:
                raise PermissionDeniedError

        return await self.repository.update(
            employee=employee,
            data=update_data,
        )
