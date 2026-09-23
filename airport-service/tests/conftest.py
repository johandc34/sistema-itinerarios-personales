import httpx
import pytest

from app.domain.models.airport import Airport


@pytest.fixture(autouse=True)
def block_external_http(monkeypatch):
    """Fail immediately if a test attempts an unmocked HTTPX network request."""
    async def blocked_async(*args, **kwargs):
        raise AssertionError("External HTTP requests must be mocked")

    def blocked_sync(*args, **kwargs):
        raise AssertionError("External HTTP requests must be mocked")

    monkeypatch.setattr(httpx.AsyncHTTPTransport, "handle_async_request", blocked_async)
    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", blocked_sync)


@pytest.fixture
def airport():
    return Airport(
        id=1,
        name="El Dorado",
        city="Bogota",
        department="Cundinamarca",
        iata_code="BOG",
        latitude=4.7016,
        longitude=-74.1469,
    )


@pytest.fixture
def external_airport():
    return {
        "id": 1,
        "name": "El Dorado",
        "city": {"name": "Bogota"},
        "department": {"name": "Cundinamarca"},
        "iataCode": "BOG",
        "latitude": 4.7016,
        "longitude": -74.1469,
    }
