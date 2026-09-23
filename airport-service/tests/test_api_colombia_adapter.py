import asyncio
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.domain.models.airport import Airport
from app.infrastructure.adapters.api_colombia_adapter import ApiColombiaAirportAdapter


@pytest.fixture
def http_client():
    with patch(
        "app.infrastructure.adapters.api_colombia_adapter.httpx.AsyncClient",
        autospec=True,
    ) as factory:
        client = AsyncMock()
        factory.return_value.__aenter__.return_value = client
        yield factory, client


def response(status, payload=None):
    return httpx.Response(
        status,
        json=payload,
        request=httpx.Request("GET", ApiColombiaAirportAdapter.BASE_URL),
    )


def test_to_domain_maps_external_fields(external_airport, airport):
    result = ApiColombiaAirportAdapter._to_domain(external_airport)

    assert isinstance(result, Airport)
    assert result == airport
    assert result.iata_code == "BOG"
    assert result.city == "Bogota"
    assert result.department == "Cundinamarca"


@pytest.mark.parametrize("nested", [None, "unexpected", {}])
def test_to_domain_handles_optional_fields(nested):
    result = ApiColombiaAirportAdapter._to_domain(
        {"id": 2, "name": "Airport", "city": nested, "department": nested}
    )

    assert result == Airport(id=2, name="Airport")


def test_to_domain_handles_absent_optional_fields():
    assert ApiColombiaAirportAdapter._to_domain(
        {"id": 2, "name": "Airport"}
    ) == Airport(id=2, name="Airport")


@pytest.mark.parametrize("empty", [False, True])
def test_get_all(http_client, external_airport, airport, empty):
    factory, client = http_client
    client.get.return_value = response(200, [] if empty else [external_airport])
    adapter = ApiColombiaAirportAdapter(timeout=3.0)

    result = asyncio.run(adapter.get_all())

    assert result == ([] if empty else [airport])
    factory.assert_called_once_with(timeout=3.0)
    client.get.assert_awaited_once_with(adapter.BASE_URL)


def test_get_by_id(http_client, external_airport, airport):
    _, client = http_client
    client.get.return_value = response(200, external_airport)
    adapter = ApiColombiaAirportAdapter()

    assert asyncio.run(adapter.get_by_id(1)) == airport
    client.get.assert_awaited_once_with(f"{adapter.BASE_URL}/1")


def test_get_by_id_returns_none_for_404(http_client):
    _, client = http_client
    client.get.return_value = response(404)
    adapter = ApiColombiaAirportAdapter()

    assert asyncio.run(adapter.get_by_id(999)) is None
    client.get.assert_awaited_once_with(f"{adapter.BASE_URL}/999")


@pytest.mark.parametrize("method, args", [("get_all", ()), ("get_by_id", (1,))])
def test_provider_http_error_is_propagated(http_client, method, args):
    _, client = http_client
    client.get.return_value = response(503)

    with pytest.raises(httpx.HTTPStatusError) as error:
        asyncio.run(getattr(ApiColombiaAirportAdapter(), method)(*args))

    assert error.value.response.status_code == 503


@pytest.mark.parametrize("method, args", [("get_all", ()), ("get_by_id", (1,))])
def test_provider_timeout_is_propagated(http_client, method, args):
    _, client = http_client
    client.get.side_effect = httpx.ReadTimeout("Provider timed out")

    with pytest.raises(httpx.ReadTimeout):
        asyncio.run(getattr(ApiColombiaAirportAdapter(), method)(*args))
