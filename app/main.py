from fastapi import FastAPI
from app.api.endpoints import router


def get_application() -> FastAPI:
    application = FastAPI(
        title="GitHub Searcher",
        version="1.0.0"
    )

    application.include_router(router, prefix="/api")

    return application


app = get_application()
