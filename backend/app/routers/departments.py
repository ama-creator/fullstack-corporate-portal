from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_current_user,
    get_department_service,
    require_roles,
)
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.services.department import DepartmentService

router = APIRouter(
    prefix="/api/v1/departments",
    tags=["Departments"],
)


@router.get(
    "",
    response_model=list[DepartmentResponse],
)
async def get_departments(
    service: Annotated[
        DepartmentService,
        Depends(get_department_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(get_current_user),
    ],
) -> list[DepartmentResponse]:
    return await service.get_all()


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
async def get_department(
    department_id: int,
    service: Annotated[
        DepartmentService,
        Depends(get_department_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(get_current_user),
    ],
) -> DepartmentResponse:
    return await service.get_by_id(department_id)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    data: DepartmentCreate,
    service: Annotated[
        DepartmentService,
        Depends(get_department_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(
            require_roles(
                EmployeeRole.ADMIN,
            )
        ),
    ],
) -> DepartmentResponse:
    return await service.create(data)


@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    service: Annotated[
        DepartmentService,
        Depends(get_department_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(
            require_roles(
                EmployeeRole.ADMIN,
            )
        ),
    ],
) -> DepartmentResponse:
    return await service.update(
        department_id=department_id,
        data=data,
    )
