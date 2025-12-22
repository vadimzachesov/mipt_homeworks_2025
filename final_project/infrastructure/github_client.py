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
    created_at: str | None = None
    homepage: str | None = None
    size: int | None = None
    open_issues_count: int | None = None
    watchers_count: int | None = None
    license_name: str | None = None
    topics: list[str] | None = None
    has_issues: bool | None = None
    has_projects: bool | None = None
    has_downloads: bool | None = None
    has_wiki: bool | None = None
    has_pages: bool | None = None
    has_discussions: bool | None = None
    fork: bool | None = None
    archived: bool | None = None
    is_template: bool | None = None
    default_branch: str | None = None


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
                created_at=item.get("created_at"),
                homepage=item.get("homepage"),
                size=item.get("size"),
                open_issues_count=item.get("open_issues_count"),
                watchers_count=item.get("watchers_count"),
                license_name=(item.get("license") or {}).get("name")
                if item.get("license") is not None
                else None,
                topics=item.get("topics")
                if item.get("topics") is not None
                else None,
                has_issues=item.get("has_issues"),
                has_projects=item.get("has_projects"),
                has_downloads=item.get("has_downloads"),
                has_wiki=item.get("has_wiki"),
                has_pages=item.get("has_pages"),
                has_discussions=item.get("has_discussions"),
                fork=item.get("fork"),
                archived=item.get("archived"),
                is_template=item.get("is_template"),
                default_branch=item.get("default_branch"),
            )
            for item in data["items"]
        ]

        return RepositorySearchResult(
            total_count=data["total_count"],
            incomplete_results=data["incomplete_results"],
            items=repositories,
        )
