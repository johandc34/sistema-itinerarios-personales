import httpx
from fastapi import APIRouter, HTTPException, status

from app.api.schemas.airport_response import AirportResponse
from app.application.services.airport_service import AirportService
from app.infrastructure.adapters.api_colombia_adapter import (
    ApiColombiaAirportAdapter,
)


router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)

repository = ApiColombiaAirportAdapter()
service = AirportService(repository)


@router.get(
    "",
    response_model=list[AirportResponse],
    summary="Consultar todos los aeropuertos"
)
async def get_airports():
    try:
        return await service.get_all_airports()

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No fue posible consultar los aeropuertos en API Colombia."
        ) from error


@router.get(
    "/{airport_id}",
    response_model=AirportResponse,
    summary="Consultar aeropuerto por identificador"
)
async def get_airport_by_id(airport_id: int):
    try:
        airport = await service.get_airport_by_id(airport_id)

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No fue posible consultar API Colombia."
        ) from error

    if airport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el aeropuerto con id {airport_id}."
        )

    return airport