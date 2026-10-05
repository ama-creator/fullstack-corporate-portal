from app.exceptions import DepartmentAlreadyExistsError, DepartmentNotFoundError
from app.models.department import Department
from app.repositories.department import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(
        self,
        repository: DepartmentRepository,
    ) -> None:
        self.repository = repository

    async def get_all(self) -> list[Department]:
        return await self.repository.get_all()

    async def get_by_id(
        self,
        department_id: int,
    ) -> Department:
        department = await self.repository.get_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError

        return department

    async def create(
        self,
        data: DepartmentCreate,
    ) -> Department:
        existing_department = await self.repository.get_by_name(data.name)

        if existing_department is not None:
            raise DepartmentAlreadyExistsError

        department = Department(
            name=data.name,
            description=data.description,
        )

        return await self.repository.create(department)

    async def update(
        self,
        department_id: int,
        data: DepartmentUpdate,
    ) -> Department:
        department = await self.repository.get_by_id(department_id)

        if department is None:
            raise DepartmentNotFoundError

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return department

        if "name" in update_data:
            existing_department = await self.repository.get_by_name(update_data["name"])

            if (
                existing_department is not None
                and existing_department.id != department.id
            ):
                raise DepartmentAlreadyExistsError

        return await self.repository.update(
            department=department,
            data=update_data,
        )
