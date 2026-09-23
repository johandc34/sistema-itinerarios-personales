from typing import Any

import httpx

from app.domain.models.airport import Airport
from app.domain.ports.airport_repository import AirportRepository


class ApiColombiaAirportAdapter(AirportRepository):
    BASE_URL = "https://api-colombia.com/api/v1/Airport"

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    async def get_all(self) -> list[Airport]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.BASE_URL)
            response.raise_for_status()

            data = response.json()

        return [self._to_domain(item) for item in data]

    async def get_by_id(self, airport_id: int) -> Airport | None:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.BASE_URL}/{airport_id}"
            )

            if response.status_code == 404:
                return None

            response.raise_for_status()

            data = response.json()

        return self._to_domain(data)

    @staticmethod
    def _to_domain(data: dict[str, Any]) -> Airport:
        city = data.get("city")
        department = data.get("department")

        city_name = (
            city.get("name")
            if isinstance(city, dict)
            else None
        )

        department_name = (
            department.get("name")
            if isinstance(department, dict)
            else None
        )

        return Airport(
            id=data["id"],
            name=data["name"],
            city=city_name,
            department=department_name,
            iata_code=data.get("iataCode"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )