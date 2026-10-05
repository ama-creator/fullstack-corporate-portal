from app.exceptions import PositionAlreadyExistsError, PositionNotFoundError
from app.models.position import Position
from app.repositories.position import PositionRepository
from app.schemas.position import PositionCreate, PositionUpdate


class PositionService:
    def __init__(
        self,
        repository: PositionRepository,
    ) -> None:
        self.repository = repository

    async def get_all(self) -> list[Position]:
        return await self.repository.get_all()

    async def get_by_id(
        self,
        position_id: int,
    ) -> Position:
        position = await self.repository.get_by_id(position_id)

        if position is None:
            raise PositionNotFoundError

        return position

    async def create(
        self,
        data: PositionCreate,
    ) -> Position:
        existing_position = await self.repository.get_by_name(data.name)

        if existing_position is not None:
            raise PositionAlreadyExistsError

        position = Position(
            name=data.name,
            description=data.description,
        )

        return await self.repository.create(position)

    async def update(
        self,
        position_id: int,
        data: PositionUpdate,
    ) -> Position:
        position = await self.repository.get_by_id(position_id)

        if position is None:
            raise PositionNotFoundError

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return position

        if "name" in update_data:
            existing_position = await self.repository.get_by_name(update_data["name"])

            if existing_position is not None and existing_position.id != position.id:
                raise PositionAlreadyExistsError

        return await self.repository.update(
            position=position,
            data=update_data,
        )
