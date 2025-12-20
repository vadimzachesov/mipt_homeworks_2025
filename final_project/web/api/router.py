from fastapi.routing import APIRouter
from final_project.web.api import monitoring, search

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(search.router, prefix="/search")
