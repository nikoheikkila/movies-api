from fastapi import FastAPI

StandardResponse = dict[str, str]

app = FastAPI()


@app.get("/")
async def root() -> StandardResponse:
    return {"title": "Movies API"}
