from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Airport:
    id: int
    name: str
    city: Optional[str] = None
    department: Optional[str] = None
    iata_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None