from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    DepartmentAlreadyExistsError,
    DepartmentNotFoundError,
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    PermissionDeniedError,
    PositionAlreadyExistsError,
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


async def department_already_exists_handler(
    _request: Request,
    _exc: DepartmentAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Department with this name already exists",
        },
    )


async def position_already_exists_handler(
    _request: Request,
    _exc: PositionAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Position with this name already exists",
        },
    )
