from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

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


class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)

    phone: str | None = Field(default=None, max_length=50)
    birth_date: date | None = None
    hire_date: date

    department_id: int | None = Field(default=None, ge=1)
    position_id: int | None = Field(default=None, ge=1)

    role: EmployeeRole = EmployeeRole.EMPLOYEE


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    middle_name: str | None = Field(
        default=None,
        max_length=100,
    )
    phone: str | None = Field(
        default=None,
        max_length=50,
    )
    birth_date: date | None = None
    hire_date: date | None = None

    department_id: int | None = Field(
        default=None,
        ge=1,
    )
    position_id: int | None = Field(
        default=None,
        ge=1,
    )

    role: EmployeeRole | None = None
    is_active: bool | None = None
