from app.domain.models.airport import Airport
from app.domain.ports.airport_repository import AirportRepository


class AirportService:

    def __init__(self, repository: AirportRepository):
        self.repository = repository

    async def get_all_airports(self) -> list[Airport]:
        return await self.repository.get_all()

    async def get_airport_by_id(
        self,
        airport_id: int
    ) -> Airport | None:
        return await self.repository.get_by_id(airport_id)