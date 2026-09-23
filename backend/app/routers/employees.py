from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_current_user, get_employee_service
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.schemas.employee import (
    EmployeeListPageResponse,
    EmployeeListResponse,
    EmployeeMeResponse,
)
from app.services.employee import EmployeeService

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"],
)


@router.get("/me", response_model=EmployeeMeResponse)
async def get_me(
    current_user: Annotated[Employee, Depends(get_current_user)],
) -> EmployeeMeResponse:
    return current_user


@router.get("/{employee_id}", response_model=EmployeeListResponse)
async def get_employee(
    employee_id: int,
    service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[Employee, Depends(get_current_user)],
) -> EmployeeListResponse:
    employee = await service.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@router.get("", response_model=EmployeeListPageResponse)
async def get_employees(
    service: Annotated[
        EmployeeService,
        Depends(get_employee_service),
    ],
    current_user: Annotated[
        Employee,
        Depends(get_current_user),
    ],
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    department_id: int | None = Query(default=None, ge=1),
    position_id: int | None = Query(default=None, ge=1),
    role: EmployeeRole | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
) -> EmployeeListPageResponse:
    employees, total = await service.get_all(
        limit=limit,
        offset=offset,
        department_id=department_id,
        position_id=position_id,
        role=role,
        is_active=is_active,
        search=search,
    )

    return EmployeeListPageResponse(
        items=employees,
        total=total,
        limit=limit,
        offset=offset,
    )
