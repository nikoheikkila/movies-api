from fastapi.testclient import TestClient
from assertpy import assert_that
import pytest

from movies_api.api import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


class TestMoviesAPI:
    def test_healthcheck_route_should_return_zero_exit_code_for_healthy_system(self, client: TestClient) -> None:
        response = client.get("/healthcheck")

        assert_that(response).has_status_code(200)
        assert_that(response.json()).is_equal_to(
            {
                "code": 0,
            }
        )

    def test_add_movies_should_return_the_movies_added(self, client: TestClient) -> None:
        payload = [
            {"name": "The Shawshank Redemption", "year": 1994, "rating": 9.3},
            {"name": "The Godfather", "year": 1972, "rating": 9.2},
        ]

        response = client.post("/movies/add", json=payload)

        assert_that(response).has_status_code(201)
        assert_that(response.json()).is_equal_to(
            {
                "success": True,
                "movies": ["The Shawshank Redemption", "The Godfather"],
            }
        )
