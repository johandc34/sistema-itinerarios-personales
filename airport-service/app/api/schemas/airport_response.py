from pydantic import BaseModel, ConfigDict


class AirportResponse(BaseModel):
    id: int
    name: str
    city: str | None = None
    department: str | None = None
    iata_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    model_config = ConfigDict(from_attributes=True)