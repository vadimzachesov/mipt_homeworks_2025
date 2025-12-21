from dataclasses import dataclass

import httpx

from final_project.infrastructure.exceptions import (
    GitHubAPIRequestError,
    GitHubAPIStatusError,
)


@dataclass
class GitHubRepository:
    """GitHub repository data."""

    id: int
    name: str
    full_name: str
    description: str | None
    html_url: str
    stargazers_count: int
    forks_count: int
    language: str | None
    updated_at: str
    owner_login: str
    owner_avatar_url: str


@dataclass
class RepositorySearchResult:
    """GitHub repository search result data."""

    total_count: int
    incomplete_results: bool
    items: list[GitHubRepository]


class GitHubClient:
    """GitHub client for interacting with the GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(
        self, http_client: httpx.AsyncClient, token: str | None = None
    ) -> None:
        self.token = token
        self._client = http_client

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
        per_page: int = 30,  # Количество репозиториев на этой странице
    ) -> RepositorySearchResult:
        """Search for repositories on GitHub."""
        url = self.BASE_URL + "/search/repositories"

        params: dict[str, str | int] = {
            "q": query,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": per_page,
        }
        try:
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code if exc.response else 500
            raise GitHubAPIStatusError(
                f"GitHub API returned error status: {status_code}",
                status_code=status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise GitHubAPIRequestError(
                f"Failed to connect to GitHub API: {exc}"
            ) from exc

        repositories = [
            GitHubRepository(
                id=item["id"],
                name=item["name"],
                full_name=item["full_name"],
                description=item.get("description"),
                html_url=item["html_url"],
                stargazers_count=item["stargazers_count"],
                forks_count=item["forks_count"],
                language=item.get("language"),
                updated_at=item["updated_at"],
                owner_login=item["owner"]["login"],
                owner_avatar_url=item["owner"]["avatar_url"],
            )
            for item in data["items"]
        ]

        return RepositorySearchResult(
            total_count=data["total_count"],
            incomplete_results=data["incomplete_results"],
            items=repositories,
        )
