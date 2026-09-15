from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.jwt import create_access_token, create_refresh_token
from app.core.security import verify_password
from app.models.employee import Employee
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenResponse:
    result = await session.execute(select(Employee).where(Employee.email == data.email))

    employee = result.scalar_one_or_none()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    access_token = create_access_token(
        subject=str(employee.id),
    )

    refresh_token = create_refresh_token(
        subject=str(employee.id),
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
