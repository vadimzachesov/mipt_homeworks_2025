from pathlib import Path

from fastapi import HTTPException

from final_project.infrastructure.exceptions import GitHubAPIError
from final_project.infrastructure.github_client import (
    GitHubClient,
    GitHubRepository,
)
from final_project.models.csv_models import RepositoryCsvRow
from final_project.services.csv_writer import CsvWriter
from final_project.services.query_builder import build_github_search_query


class SearchService:
    """Search service for searching repositories on GitHub."""

    def __init__(
        self, github_client: GitHubClient, csv_writer: CsvWriter
    ) -> None:
        self.client = github_client
        self.csv_writer = csv_writer

    async def create_search_report(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int = 0,
        stars_max: int | None = None,
        forks_min: int = 0,
        forks_max: int | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
    ) -> str:
        """Create a search report for repositories on GitHub."""
        final_query = build_github_search_query(
            lang=lang,
            stars_min=stars_min,
            stars_max=stars_max,
            forks_min=forks_min,
            forks_max=forks_max,
            created_from=created_from,
            created_to=created_to,
        )

        all_items: list[GitHubRepository] = []
        page = 1
        target_count = offset + limit

        while len(all_items) < target_count:
            try:
                data = await self.client.search_repositories(
                    query=final_query, page=page, per_page=100
                )
            except GitHubAPIError as exc:
                status_code = exc.status_code if exc.status_code else 502
                raise HTTPException(
                    status_code=status_code, detail=exc.message
                ) from exc

            if not data.items:
                break

            all_items.extend(data.items)
            page += 1

            if len(data.items) < 100:
                break

        sliced_items = all_items[offset: offset + limit]

        csv_rows = [
            RepositoryCsvRow.from_github_repository(repo)
            for repo in sliced_items
        ]

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        file_path = Path("static") / filename

        try:
            await self.csv_writer.write_repositories_csv(csv_rows, file_path)
        except Exception as exc:
            raise HTTPException(
                status_code=500, detail=f"Failed to save CSV: {exc}"
            ) from exc

        return filename
