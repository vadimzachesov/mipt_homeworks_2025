import logging
import traceback
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from final_project.infrastructure.github_client import GitHubClient
from final_project.services.csv_writer import CsvWriter
from final_project.services.search_service import SearchService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_github_client(request: Request) -> GitHubClient:
    """Get the GitHub client from the request."""
    return request.app.state.github_client


def get_csv_writer() -> CsvWriter:
    """Get the CSV writer."""
    return CsvWriter()


def get_search_service(
    github_client: GitHubClient = Depends(get_github_client),
    csv_writer: CsvWriter = Depends(get_csv_writer)
) -> SearchService:
    """Get the search service."""
    return SearchService(github_client=github_client, csv_writer=csv_writer)


@router.post("", status_code=201)
async def search_repositories(
    limit: int = Query(..., ge=1, description="Сколько репозиториев вернуть"),
    offset: int = Query(0, ge=0, description="Сколько пропустить"),
    lang: str = Query(..., description="Язык программирования"),
    stars_min: int = Query(0, ge=0),
    stars_max: int = Query(None, ge=0),
    forks_min: int = Query(0, ge=0),
    forks_max: int = Query(None, ge=0),
    created_from: str | None = Query(None, description="Дата создания от (YYYY-MM-DD)"),
    created_to: str | None = Query(None, description="Дата создания до (YYYY-MM-DD)"),
    service: SearchService = Depends(get_search_service)
) -> dict[str, Any]:
    """Search for repositories on GitHub."""
    try:
        filename = await service.create_search_report(
            limit=limit,
            offset=offset,
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            created_from=created_from,
            created_to=created_to
        )

        return {
            "status": "success",
            "message": "File created successfully",
            "filename": filename
        }
    except HTTPException:
        raise
    except Exception as exc:
        tb = traceback.format_exc()
        logger.error("Unhandled exception in search_repositories: %s\n%s", exc, tb)
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}") \
        from exc
