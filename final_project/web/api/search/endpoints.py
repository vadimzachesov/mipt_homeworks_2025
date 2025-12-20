from fastapi import APIRouter, Query, Depends
from final_project.services.search_service import SearchService

router = APIRouter()


@router.post("", status_code=201)
async def search_repositories(
        limit: int = Query(..., ge=1, description="Сколько репозиториев вернуть"),
        offset: int = Query(0, ge=0, description="Сколько пропустить"),
        lang: str = Query(..., description="Язык программирования"),
        stars_min: int = Query(0, ge=0),
        stars_max: int = Query(None, ge=0),
        forks_min: int = Query(0, ge=0),
        forks_max: int = Query(None, ge=0),
        service: SearchService = Depends()
):
    filename = await service.create_search_report(
        limit=limit,
        offset=offset,
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max
    )

    return {
        "status": "success",
        "message": "File created successfully",
        "filename": filename
    }
