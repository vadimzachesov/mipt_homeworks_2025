import httpx
from typing import Dict, Any, Optional, Union


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "FastAPI-Template-Searcher",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    async def search_repositories(
            self,
            query: str,
            sort: str = "stars",
            order: str = "desc",
            page: int = 1,  # Номер страницы результатов
            per_page: int = 30  # Количество репозиториев на этой странице
    ) -> Dict[str, Any]:
        url = self.BASE_URL + "/search/repositories"

        params: Dict[str, Union[str, int]] = {
            "q": query,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": per_page
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Выбросит ошибку, если статус не 200
            return response.json()
