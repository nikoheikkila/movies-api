import pytest

from movies_api.repository import FakeMovieRepository


@pytest.fixture()
def repository() -> FakeMovieRepository:
    return FakeMovieRepository()
