from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    DepartmentNotFoundError,
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    PermissionDeniedError,
    PositionNotFoundError,
    SelfModificationError,
)


async def employee_already_exists_handler(
    request: Request,
    exc: EmployeeAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Employee with this email already exists",
        },
    )


async def department_not_found_handler(
    request: Request,
    exc: DepartmentNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Department not found",
        },
    )


async def position_not_found_handler(
    request: Request,
    exc: PositionNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Position not found",
        },
    )


async def permission_denied_handler(
    _request: Request,
    _exc: PermissionDeniedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "You do not have permission to assign this role",
        },
    )


async def employee_not_found_handler(
    _request: Request,
    _exc: EmployeeNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Employee not found",
        },
    )


async def self_modification_handler(
    _request: Request,
    _exc: SelfModificationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": (
                "Administrator cannot remove their own admin role "
                "or deactivate their own account"
            ),
        },
    )
