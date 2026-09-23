import asyncio
from unittest.mock import create_autospec

import pytest

from app.application.services.airport_service import AirportService
from app.domain.ports.airport_repository import AirportRepository


@pytest.fixture
def repository():
    return create_autospec(AirportRepository, instance=True)


@pytest.mark.parametrize("empty", [False, True])
def test_get_all_airports(repository, airport, empty):
    expected = [] if empty else [airport]
    repository.get_all.return_value = expected

    result = asyncio.run(AirportService(repository).get_all_airports())

    assert result == expected
    repository.get_all.assert_awaited_once_with()
    repository.get_by_id.assert_not_called()


@pytest.mark.parametrize("exists", [True, False])
def test_get_airport_by_id(repository, airport, exists):
    expected = airport if exists else None
    repository.get_by_id.return_value = expected

    result = asyncio.run(AirportService(repository).get_airport_by_id(1))

    assert result == expected
    repository.get_by_id.assert_awaited_once_with(1)
    repository.get_all.assert_not_called()
