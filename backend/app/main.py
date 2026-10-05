from fastapi import FastAPI

from app.exception_handlers import (
    department_already_exists_handler,
    department_not_found_handler,
    employee_already_exists_handler,
    employee_not_found_handler,
    permission_denied_handler,
    position_already_exists_handler,
    position_not_found_handler,
    self_modification_handler,
)
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
from app.routers.auth import router as auth_router
from app.routers.departments import router as departments_router
from app.routers.employees import router as employees_router
from app.routers.health import router as health_router
from app.routers.positions import router as positions_router

app = FastAPI(
    title="Corporate Portal API",
    description="Production-like corporate portal backend",
    version="1.0.0",
)

app.add_exception_handler(
    EmployeeAlreadyExistsError,
    employee_already_exists_handler,
)

app.add_exception_handler(
    PermissionDeniedError,
    permission_denied_handler,
)

app.add_exception_handler(
    DepartmentNotFoundError,
    department_not_found_handler,
)

app.add_exception_handler(
    EmployeeNotFoundError,
    employee_not_found_handler,
)

app.add_exception_handler(
    PositionNotFoundError,
    position_not_found_handler,
)

app.add_exception_handler(
    SelfModificationError,
    self_modification_handler,
)

app.add_exception_handler(
    DepartmentAlreadyExistsError,
    department_already_exists_handler,
)

app.add_exception_handler(
    PositionAlreadyExistsError,
    position_already_exists_handler,
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(departments_router)
app.include_router(positions_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
