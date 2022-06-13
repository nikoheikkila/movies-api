from fastapi.testclient import TestClient
from assertpy import assert_that
import pytest

from movies_api.api import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


class TestMoviesAPI:
    def test_root_route_should_return_ok_response(self, client: TestClient) -> None:
        response = client.get("/")

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).contains_key("title").contains_value("Movies API")
