from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.employee import Employee
from app.schemas.employee import EmployeeMeResponse

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"],
)


@router.get("/me", response_model=EmployeeMeResponse)
async def get_me(
    current_user: Annotated[Employee, Depends(get_current_user)],
) -> EmployeeMeResponse:
    return current_user
