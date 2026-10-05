from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_current_user,
    get_position_service,
    require_roles,
)
from app.models.employee import Employee
from app.models.enums import EmployeeRole
from app.schemas.position import PositionCreate, PositionResponse, PositionUpdate
from app.services.position import PositionService

router = APIRouter(
    prefix="/api/v1/positions",
    tags=["Positions"],
)


@router.get(
    "",
    response_model=list[PositionResponse],
)
async def get_positions(
    service: Annotated[
        PositionService,
        Depends(get_position_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(get_current_user),
    ],
) -> list[PositionResponse]:
    return await service.get_all()


@router.get(
    "/{position_id}",
    response_model=PositionResponse,
)
async def get_position(
    position_id: int,
    service: Annotated[
        PositionService,
        Depends(get_position_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(get_current_user),
    ],
) -> PositionResponse:
    return await service.get_by_id(position_id)


@router.post(
    "",
    response_model=PositionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_position(
    data: PositionCreate,
    service: Annotated[
        PositionService,
        Depends(get_position_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(
            require_roles(
                EmployeeRole.ADMIN,
            )
        ),
    ],
) -> PositionResponse:
    return await service.create(data)


@router.patch(
    "/{position_id}",
    response_model=PositionResponse,
)
async def update_position(
    position_id: int,
    data: PositionUpdate,
    service: Annotated[
        PositionService,
        Depends(get_position_service),
    ],
    _current_user: Annotated[
        Employee,
        Depends(
            require_roles(
                EmployeeRole.ADMIN,
            )
        ),
    ],
) -> PositionResponse:
    return await service.update(
        position_id=position_id,
        data=data,
    )
