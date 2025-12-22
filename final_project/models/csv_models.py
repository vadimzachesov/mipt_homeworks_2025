from __future__ import annotations

from dataclasses import dataclass

from final_project.infrastructure.github_client import GitHubRepository


@dataclass
class RepositoryCsvRow:
    """Repository data for CSV export."""

    name: str
    description: str | None
    url: str
    created_at: str | None
    updated_at: str | None
    homepage: str | None
    size: int | None
    stars: int | None
    forks: int | None
    issues: int | None
    watchers: int | None
    language: str | None
    license: str | None
    topics: str | None
    has_issues: bool | None
    has_projects: bool | None
    has_downloads: bool | None
    has_wiki: bool | None
    has_pages: bool | None
    has_discussions: bool | None
    is_fork: bool | None
    is_archived: bool | None
    is_template: bool | None
    default_branch: str | None

    @classmethod
    def get_fieldnames(cls) -> list[str]:
        """Get field names for CSV export in the requested order."""
        return [
            "Name",
            "Description",
            "URL",
            "Created At",
            "Updated At",
            "Homepage",
            "Size",
            "Stars",
            "Forks",
            "Issues",
            "Watchers",
            "Language",
            "License",
            "Topics",
            "Has Issues",
            "Has Projects",
            "Has Downloads",
            "Has Wiki",
            "Has Pages",
            "Has Discussions",
            "Is Fork",
            "Is Archived",
            "Is Template",
            "Default Branch",
        ]

    @classmethod
    def from_github_repository(
        cls, repo: GitHubRepository
    ) -> RepositoryCsvRow:
        """Create a RepositoryCsvRow from a GitHubRepository."""
        topics_list = getattr(repo, "topics", None)
        topics = ";".join(topics_list) if topics_list else None

        return cls(
            name=repo.name,
            description=repo.description,
            url=repo.html_url,
            created_at=getattr(repo, "created_at", None),
            updated_at=getattr(repo, "updated_at", None),
            homepage=getattr(repo, "homepage", None),
            size=getattr(repo, "size", None),
            stars=getattr(repo, "stargazers_count", None),
            forks=getattr(repo, "forks_count", None),
            issues=getattr(repo, "open_issues_count", None),
            watchers=getattr(repo, "watchers_count", None),
            language=repo.language,
            license=(getattr(repo, "license_name", None) or None),
            topics=topics,
            has_issues=getattr(repo, "has_issues", None),
            has_projects=getattr(repo, "has_projects", None),
            has_downloads=getattr(repo, "has_downloads", None),
            has_wiki=getattr(repo, "has_wiki", None),
            has_pages=getattr(repo, "has_pages", None),
            has_discussions=getattr(repo, "has_discussions", None),
            is_fork=getattr(repo, "fork", None),
            is_archived=getattr(repo, "archived", None),
            is_template=getattr(repo, "is_template", None),
            default_branch=getattr(repo, "default_branch", None),
        )
