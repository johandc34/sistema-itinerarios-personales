from unittest.mock import create_autospec

import httpx
import pytest
from fastapi.testclient import TestClient

from app.api.routes import airports
from app.domain.ports.airport_repository import AirportRepository
from app.main import app


@pytest.fixture
def repository(monkeypatch):
    mock = create_autospec(AirportRepository, instance=True)
    monkeypatch.setattr(airports.service, "repository", mock)
    return mock


@pytest.fixture
def client(repository):
    # Exercise the real routes, application service and response serialization.
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def expected_airport():
    return {
        "id": 1,
        "name": "El Dorado",
        "city": "Bogota",
        "department": "Cundinamarca",
        "iata_code": "BOG",
        "latitude": 4.7016,
        "longitude": -74.1469,
    }


def test_root(client):
    result = client.get("/")

    assert result.status_code == 200
    assert result.json() == {"message": "Airport Service funcionando correctamente"}


def test_health(client):
    result = client.get("/health")

    assert result.status_code == 200
    assert result.json() == {"status": "ok", "service": "airport-service"}


def test_get_airports(client, repository, airport, expected_airport):
    repository.get_all.return_value = [airport]

    result = client.get("/airports")

    assert result.status_code == 200
    assert result.json() == [expected_airport]
    repository.get_all.assert_awaited_once_with()


def test_get_airports_empty(client, repository):
    repository.get_all.return_value = []

    result = client.get("/airports")

    assert result.status_code == 200
    assert result.json() == []


def test_get_airport_by_id(client, repository, airport, expected_airport):
    repository.get_by_id.return_value = airport

    result = client.get("/airports/1")

    assert result.status_code == 200
    assert result.json() == expected_airport
    repository.get_by_id.assert_awaited_once_with(1)


def test_get_airport_not_found(client, repository):
    repository.get_by_id.return_value = None

    result = client.get("/airports/999")

    assert result.status_code == 404
    assert result.json() == {"detail": "No se encontró el aeropuerto con id 999."}
    repository.get_by_id.assert_awaited_once_with(999)


@pytest.mark.parametrize(
    "path, method, detail",
    [
        ("/airports", "get_all", "No fue posible consultar los aeropuertos en API Colombia."),
        ("/airports/1", "get_by_id", "No fue posible consultar API Colombia."),
    ],
)
@pytest.mark.parametrize("failure", ["http_status", "timeout", "connection"])
def test_provider_error_returns_502(client, repository, path, method, detail, failure):
    request = httpx.Request("GET", "https://provider.invalid/airports")
    errors = {
        "http_status": httpx.HTTPStatusError(
            "Unavailable", request=request, response=httpx.Response(503, request=request)
        ),
        "timeout": httpx.ReadTimeout("Timed out", request=request),
        "connection": httpx.ConnectError("Connection failed", request=request),
    }
    getattr(repository, method).side_effect = errors[failure]

    result = client.get(path)

    assert result.status_code == 502
    assert result.json() == {"detail": detail}
    getattr(repository, method).assert_awaited_once_with(*(() if method == "get_all" else (1,)))
