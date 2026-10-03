from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.jwt import decode_access_token
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.repositories.position import PositionRepository
from app.services.employee import EmployeeService

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Employee:
    token = credentials.credentials

    payload = decode_access_token(token)

    subject = payload.get("sub")

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await session.execute(
        select(Employee).where(
            Employee.id == int(subject),
        )
    )

    employee = result.scalar_one_or_none()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return employee


def get_employee_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> EmployeeRepository:
    return EmployeeRepository(session)


async def get_employee_service(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> EmployeeService:
    return EmployeeService(
        repository=EmployeeRepository(session),
        department_repository=DepartmentRepository(session),
        position_repository=PositionRepository(session),
    )


def require_roles(*allowed_roles: EmployeeRole):
    async def role_checker(
        current_user: Annotated[
            Employee,
            Depends(get_current_user),
        ],
    ) -> Employee:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
