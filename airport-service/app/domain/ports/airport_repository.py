from abc import ABC, abstractmethod

from app.domain.models.airport import Airport


class AirportRepository(ABC):

    @abstractmethod
    async def get_all(self) -> list[Airport]:
        pass

    @abstractmethod
    async def get_by_id(self, airport_id: int) -> Airport | None:
        pass