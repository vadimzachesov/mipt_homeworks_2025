from __future__ import annotations

from dataclasses import dataclass, fields

from final_project.infrastructure.github_client import GitHubRepository


@dataclass
class RepositoryCsvRow:
    """Repository data for CSV export."""

    name: str
    description: str | None
    url: str
    updated_at: str
    stars: int
    forks: int
    language: str | None

    @classmethod
    def get_fieldnames(cls) -> list[str]:
        """Get field names for CSV export."""
        return [field.name.replace("_", " ").title() for field in fields(cls)]

    @classmethod
    def from_github_repository(cls, repo: GitHubRepository) -> RepositoryCsvRow:
        """Create a RepositoryCsvRow from a GitHubRepository."""
        return cls(
            name=repo.name,
            description=repo.description,
            url=repo.html_url,
            updated_at=repo.updated_at,
            stars=repo.stargazers_count,
            forks=repo.forks_count,
            language=repo.language,
        )
