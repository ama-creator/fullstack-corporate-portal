from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.enums import EmployeeRole


class EmployeeMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    middle_name: str | None
    phone: str | None
    avatar_url: str | None
    birth_date: date | None
    hire_date: date
    role: EmployeeRole
    is_active: bool


class EmployeeListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    middle_name: str | None
    avatar_url: str | None
    role: EmployeeRole
    is_active: bool


class EmployeeListPageResponse(BaseModel):
    items: list[EmployeeListResponse]
    total: int
    limit: int
    offset: int
