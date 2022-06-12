"""Tests for adding movies"""

from decimal import Decimal
from assertpy import assert_that
import pytest

from movies_api.models import Movie
from movies_api.service import MovieService
from movies_api.repository import FakeMovieRepository


@pytest.fixture()
def service(repository: FakeMovieRepository) -> MovieService:
    return MovieService(repository)


class TestAddMovies:
    def test_can_add_one_movie(self, service: MovieService) -> None:
        movie = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))

        first, *_ = service.add_movies(movie)

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)

    def test_can_add_multiple_movies(self, service: MovieService) -> None:
        movie1 = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))
        movie2 = Movie(name="The Matrix Reloaded", year=2003, rating=Decimal(7.7))

        first, second = service.add_movies(movie1, movie2)

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)
        assert_that(second).has_name("The Matrix Reloaded").has_year(2003).has_rating(7.7)
