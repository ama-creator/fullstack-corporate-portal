from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_current_user, get_employee_service
from app.models.employee import Employee
from app.schemas.employee import EmployeeListResponse, EmployeeMeResponse
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


@router.get("", response_model=list[EmployeeListResponse])
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
) -> list[EmployeeListResponse]:
    return await service.get_all(limit=limit, offset=offset)
