from fastapi import FastAPI
from pydantic import BaseModel, Field, StrictBool

from movies_api.service import MovieService
from movies_api.repository import MovieRepository
from movies_api.models import Movie

app = FastAPI()


class HealthCheckResponse(BaseModel):
    code: int = Field(..., ge=0, description="Health check response code")


class AddMoviesRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Movie title")
    year: int = Field(..., ge=1900, le=2050, description="Movie release year")
    rating: float = Field(..., ge=0.0, le=10.0, description="Movie rating")


class AddMoviesResponse(BaseModel):
    success: StrictBool = Field(default=True, description="Success flag")
    movies: list[str] = Field(default=[], description="List of added movies")


@app.get("/healthcheck", response_model=HealthCheckResponse)
def healthcheck() -> HealthCheckResponse:
    return HealthCheckResponse(code=0)


@app.post("/movies/add", status_code=201, response_model=AddMoviesResponse)
def add_movies(request: list[AddMoviesRequest]) -> AddMoviesResponse:
    service = MovieService(MovieRepository.with_memory())
    models = [Movie(**item.dict()) for item in request]

    service.add_movies(*models)
    movies = service.list()

    return AddMoviesResponse(success=True, movies=[movie.name for movie in movies])
